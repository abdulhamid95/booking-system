from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id', 'name', 'description',
            'duration_minutes', 'price', 'is_active', 'created_at',
        )
        read_only_fields = ('id', 'created_at')


class PublicServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'duration_minutes', 'price')

    def validate_duration_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError('Duration must be greater than zero.')
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Price cannot be negative.')
        return value
