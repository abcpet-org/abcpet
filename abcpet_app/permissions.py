from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Permiso personalizado que solo permite el acceso a superusuarios.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser