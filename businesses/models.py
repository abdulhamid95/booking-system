from django.conf import settings
from django.db import models


class Business(models.Model):
    class BusinessType(models.TextChoices):
        SALON = 'salon', 'Salon'
        CLINIC = 'clinic', 'Clinic'
        OTHER = 'other', 'Other'

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business',
    )
    name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=20, choices=BusinessType.choices)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return self.name