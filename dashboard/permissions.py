from rest_framework.permissions import BasePermission, IsAuthenticated

class IsSuperUser(BasePermission):
    """
    Allow access only to superusers
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser and request.user.is_authenticated

