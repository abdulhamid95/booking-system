from django.core.exceptions import ValidationError


def validate_no_overlap(staff_member_id, start_time, end_time, exclude_pk=None):
    from .models import Booking

    qs = Booking.objects.filter(
        staff_member_id=staff_member_id,
        start_time__lt=end_time,
        end_time__gt=start_time,
    ).exclude(status=Booking.Status.CANCELLED)

    if exclude_pk is not None:
        qs = qs.exclude(pk=exclude_pk)

    if qs.exists():
        raise ValidationError('هذا الموظف لديه حجز آخر في نفس الوقت.')


def validate_staff_service_match(staff_member, service):
    if not staff_member.services.filter(pk=service.pk).exists():
        raise ValidationError(
            f'الموظف "{staff_member.name}" لا يقدم خدمة "{service.name}".'
        )


def validate_booking_business_scope(business_id, staff_member, service):
    errors = []
    if staff_member.business_id != business_id:
        errors.append(f'الموظف "{staff_member.name}" لا ينتمي إلى هذه المنشأة.')
    if service.business_id != business_id:
        errors.append(f'الخدمة "{service.name}" لا تنتمي إلى هذه المنشأة.')
    if errors:
        raise ValidationError(errors)
