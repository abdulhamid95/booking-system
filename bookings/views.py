from datetime import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from services.models import Service
from staff.models import StaffMember

from .serializers import BookingCreateSerializer, BookingResponseSerializer
from .slots import get_available_slots


class PublicBookingCreateView(APIView):
    """
    POST /api/bookings/
    Public endpoint — no authentication required.
    Business is derived from the chosen service, not supplied by the client.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response(
            BookingResponseSerializer(booking).data,
            status=status.HTTP_201_CREATED,
        )


class PublicAvailableSlotsView(APIView):
    """
    GET /api/bookings/available-slots/
        ?business_id=<id>&service_id=<id>&staff_id=<id>&date=YYYY-MM-DD

    Public endpoint — returns available time slots for a staff member on a given date.
    Working hours: 09:00–18:00 (fixed for MVP).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        business_id = request.query_params.get('business_id')
        service_id = request.query_params.get('service_id')
        staff_id = request.query_params.get('staff_id')
        date_str = request.query_params.get('date')

        if not all([business_id, service_id, staff_id, date_str]):
            return Response(
                {'detail': 'business_id, service_id, staff_id, and date are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'date': 'Invalid format. Use YYYY-MM-DD.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if date < timezone.localdate():
            return Response(
                {'date': 'Date cannot be in the past.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = Service.objects.filter(
            pk=service_id, business_id=business_id, is_active=True,
        ).first()
        if service is None:
            return Response(
                {'service': 'Service not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        staff = StaffMember.objects.filter(
            pk=staff_id, business_id=business_id, is_active=True, services=service,
        ).first()
        if staff is None:
            return Response(
                {'staff_member': 'Staff member not found or does not provide this service.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        slots = get_available_slots(staff.id, service.duration_minutes, date)
        return Response({
            'date': date_str,
            'slots': [s.isoformat() for s in slots],
        })
