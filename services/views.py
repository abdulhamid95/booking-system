from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from businesses.mixins import BusinessScopedMixin

from .models import Service
from .serializers import PublicServiceSerializer, ServiceSerializer


class ServiceListCreateView(BusinessScopedMixin, ListCreateAPIView):
    """
    GET  /api/services/        — list all services for the authenticated business
    POST /api/services/        — create a new service
    """
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(business=self.get_business())

    def perform_create(self, serializer):
        serializer.save(business=self.get_business())


class ServiceDetailView(BusinessScopedMixin, RetrieveUpdateAPIView):
    """
    GET   /api/services/<id>/  — retrieve a single service
    PATCH /api/services/<id>/  — update name, description, duration, price
    """
    serializer_class = ServiceSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        return Service.objects.filter(business=self.get_business())


class PublicServiceListView(ListAPIView):
    """
    GET /api/services/public/<business_id>/
    Public endpoint — returns active services for the given business.
    """
    serializer_class = PublicServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Service.objects.filter(
            business_id=self.kwargs['business_id'],
            is_active=True,
        )


class ServiceToggleView(BusinessScopedMixin, APIView):
    """
    POST /api/services/<id>/deactivate/ — soft-disable a service
    POST /api/services/<id>/activate/   — re-enable a service
    """

    def _get_service(self, pk):
        return Service.objects.filter(
            pk=pk, business=self.get_business()
        ).first()

    def post(self, request, pk, action):
        service = self._get_service(pk)
        if service is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if action == 'deactivate':
            service.is_active = False
        elif action == 'activate':
            service.is_active = True
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service.save(update_fields=['is_active'])
        return Response(ServiceSerializer(service).data)
