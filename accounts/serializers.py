from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers

from businesses.models import Business
from businesses.serializers import BusinessSerializer

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'password')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account is disabled.')
        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'full_name', 'date_joined')
        read_only_fields = ('id', 'email', 'date_joined')


class BusinessRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField(max_length=150, required=False, allow_blank=True, default='')
    business_name = serializers.CharField(max_length=200)
    business_type = serializers.ChoiceField(choices=Business.BusinessType.choices)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, default='')
    address = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    @transaction.atomic
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
        )
        Business.objects.create(
            owner=user,
            name=validated_data['business_name'],
            business_type=validated_data['business_type'],
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
        )
        return user
