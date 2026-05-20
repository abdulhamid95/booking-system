from rest_framework import serializers as drf_serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, inline_serializer

from businesses.serializers import BusinessSerializer

from .serializers import (
    BusinessRegistrationSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: inline_serializer('RegisterResponse', fields={
            'token': drf_serializers.CharField(),
            'user': UserProfileSerializer(),
        })},
        tags=['auth'],
        summary='Register a new user account',
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'user': UserProfileSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: inline_serializer('LoginResponse', fields={
            'token': drf_serializers.CharField(),
            'user': UserProfileSerializer(),
        })},
        tags=['auth'],
        summary='Obtain an authentication token',
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserProfileSerializer(user).data})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={204: None},
        tags=['auth'],
        summary='Invalidate the current auth token',
    )
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=UserProfileSerializer,
        tags=['auth'],
        summary='Retrieve the authenticated user profile',
    )
    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)

    @extend_schema(
        request=UserProfileSerializer,
        responses=UserProfileSerializer,
        tags=['auth'],
        summary='Update the authenticated user profile',
    )
    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BusinessRegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=BusinessRegistrationSerializer,
        responses={201: inline_serializer('BusinessRegisterResponse', fields={
            'token': drf_serializers.CharField(),
            'user': UserProfileSerializer(),
            'business': BusinessSerializer(),
        })},
        tags=['auth'],
        summary='Register a new business owner account',
    )
    def post(self, request):
        serializer = BusinessRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': UserProfileSerializer(user).data,
                'business': BusinessSerializer(user.business).data,
            },
            status=status.HTTP_201_CREATED,
        )
