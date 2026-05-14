import uuid

from django.db import models
from django.utils import timezone

from businesses.models import Business
from services.models import Service
from staff.models import StaffMember


class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='bookings',
    )
    staff_member = models.ForeignKey(
        StaffMember,
        on_delete=models.PROTECT,
        related_name='bookings',
    )

    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CONFIRMED,
    )
    notes = models.TextField(blank=True)
    reference_code = models.CharField(max_length=12, unique=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-start_time']

    def clean(self):
        from .validators import (
            validate_booking_business_scope,
            validate_no_overlap,
            validate_staff_service_match,
        )
        if all([self.business_id, self.staff_member_id, self.service_id]):
            validate_booking_business_scope(self.business_id, self.staff_member, self.service)
            validate_staff_service_match(self.staff_member, self.service)

        if all([self.staff_member_id, self.start_time, self.end_time]):
            validate_no_overlap(
                self.staff_member_id, self.start_time, self.end_time,
                exclude_pk=self.pk,
            )

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = uuid.uuid4().hex[:12].upper()
        if not self.end_time and self.start_time and self.service_id:
            minutes = self.service.duration_minutes
            self.end_time = self.start_time + timezone.timedelta(minutes=minutes)
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.reference_code} — {self.customer_name} @ {self.start_time:%Y-%m-%d %H:%M}'
