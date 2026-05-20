from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view

from businesses.mixins import BusinessScopedMixin

from .models import StaffMember
from .serializers import PublicStaffSerializer, StaffMemberSerializer


@extend_schema_view(
    get=extend_schema(tags=['staff'], summary='List all staff members for the authenticated business'),
    post=extend_schema(tags=['staff'], summary='Add a new staff member'),
)
class StaffListCreateView(BusinessScopedMixin, ListCreateAPIView):
    """
    GET  /api/staff/   — list all staff members for the authenticated business
    POST /api/staff/   — add a new staff member (with optional service assignments)
    """
    serializer_class = StaffMemberSerializer

    def get_queryset(self):
        return StaffMember.objects.filter(
            business=self.get_business()
        ).prefetch_related('services')

    def perform_create(self, serializer):
        serializer.save(business=self.get_business())


@extend_schema_view(
    get=extend_schema(tags=['staff'], summary='Retrieve a staff member'),
    patch=extend_schema(tags=['staff'], summary='Update a staff member'),
)
class StaffDetailView(BusinessScopedMixin, RetrieveUpdateAPIView):
    """
    GET   /api/staff/<id>/  — retrieve a staff member
    PATCH /api/staff/<id>/  — update name, email, phone, or linked services
    """
    serializer_class = StaffMemberSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        return StaffMember.objects.filter(
            business=self.get_business()
        ).prefetch_related('services')


@extend_schema_view(
    get=extend_schema(tags=['staff'], summary='List active staff for a service within a business (public)'),
)
class PublicStaffListView(ListAPIView):
    """
    GET /api/staff/public/<business_id>/<service_id>/
    Public endpoint — returns active staff linked to the given service within the given business.
    """
    serializer_class = PublicStaffSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return StaffMember.objects.filter(
            business_id=self.kwargs['business_id'],
            services__id=self.kwargs['service_id'],
            is_active=True,
        )


class StaffToggleView(BusinessScopedMixin, APIView):
    """
    POST /api/staff/<id>/activate/   — re-enable a staff member
    POST /api/staff/<id>/deactivate/ — soft-disable a staff member
    """

    def _get_staff(self, pk):
        return StaffMember.objects.filter(
            pk=pk, business=self.get_business()
        ).first()

    @extend_schema(
        operation_id='staff_toggle',
        request=None,
        responses={200: StaffMemberSerializer},
        tags=['staff'],
        summary='Activate or deactivate a staff member',
    )
    def post(self, request, pk, action):
        member = self._get_staff(pk)
        if member is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if action == 'activate':
            member.is_active = True
        elif action == 'deactivate':
            member.is_active = False
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        member.save(update_fields=['is_active'])
        return Response(StaffMemberSerializer(member, context={'request': request}).data)
