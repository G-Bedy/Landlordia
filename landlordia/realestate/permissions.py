from rest_framework import permissions

class IsAdminOrOwner(permissions.BasePermission):
    """
    Доступ только админам и собственникам недвижки.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj.owner == request.user
