from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import BusinessScopedMixin
from .serializers import BusinessSerializer


class BusinessProfileView(BusinessScopedMixin, APIView):
    """
    GET  /api/businesses/me/  — retrieve own business profile
    PATCH /api/businesses/me/ — update own business profile
    """

    def get(self, request):
        return Response(BusinessSerializer(self.get_business()).data)

    def patch(self, request):
        serializer = BusinessSerializer(
            self.get_business(),
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)