from .permissions import IsBusinessOwner


class BusinessScopedMixin:
    """
    Mixin for any APIView or ViewSet that operates on business-owned data.

    Usage in EPIC-04/05/06:
        class ServiceListView(BusinessScopedMixin, ListCreateAPIView):
            def get_queryset(self):
                return Service.objects.filter(business=self.get_business())

    Guarantees:
    - 403 if the user is not authenticated or has no business.
    - 404 (not 403) when accessing an object from another business, because
      get_queryset() is already scoped — the object simply won't exist in results.
    """
    permission_classes = [IsBusinessOwner]

    def get_business(self):
        return self.request.user.business