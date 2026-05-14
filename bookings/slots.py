from datetime import datetime, time, timedelta

from django.utils import timezone

# Fixed working hours for MVP — extend via BusinessHours model when needed.
WORK_START = time(9, 0)
WORK_END = time(18, 0)


def get_available_slots(staff_member_id, duration_minutes, date):
    """
    Returns a list of timezone-aware datetimes representing available booking slots
    for a given staff member on a given date.

    Slot interval equals the service duration. Slots that overlap with any
    non-cancelled booking for this staff member are excluded.
    """
    from .models import Booking

    tz = timezone.get_current_timezone()

    day_start = timezone.make_aware(datetime.combine(date, WORK_START), tz)
    day_end = timezone.make_aware(datetime.combine(date, WORK_END), tz)

    existing = list(
        Booking.objects.filter(
            staff_member_id=staff_member_id,
            start_time__date=date,
        )
        .exclude(status=Booking.Status.CANCELLED)
        .values_list('start_time', 'end_time')
    )

    duration = timedelta(minutes=duration_minutes)
    slots = []
    current = day_start

    while current + duration <= day_end:
        slot_end = current + duration
        overlaps = any(
            current < booking_end and slot_end > booking_start
            for booking_start, booking_end in existing
        )
        if not overlaps:
            slots.append(current)
        current += duration

    return slots
