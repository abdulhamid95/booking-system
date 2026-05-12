from rest_framework.permissions import BasePermission


class IsBusinessOwner(BasePermission):
    """
    Grants access only to authenticated users who own a business.
    Returns 403 if the user is not authenticated or has no associated business.
    """
    message = 'You do not have a business account.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'business')
        )