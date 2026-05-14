from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            'service', 'staff_member',
            'customer_name', 'customer_phone', 'customer_email',
            'start_time', 'notes',
        )

    def validate(self, data):
        service = data.get('service')
        staff_member = data.get('staff_member')
        if service and not service.is_active:
            raise serializers.ValidationError({'service': 'هذه الخدمة غير متاحة حالياً.'})
        if staff_member and not staff_member.is_active:
            raise serializers.ValidationError({'staff_member': 'هذا الموظف غير متاح حالياً.'})
        return data

    def create(self, validated_data):
        service = validated_data['service']
        booking = Booking(business=service.business, **validated_data)
        try:
            booking.save()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                exc.message_dict if hasattr(exc, 'message_dict') else exc.messages
            )
        return booking


class BookingResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            'reference_code',
            'service', 'staff_member',
            'customer_name', 'customer_phone', 'customer_email',
            'start_time', 'end_time',
            'status', 'notes',
        )
