from rest_framework import permissions

from realestate.models import LeaseContract


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


class IsAdminOrLeaseContractOwner(permissions.BasePermission):
    """
    Проверяет, связан ли пользователь с объектом LeaseContract
    через Property.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj.property.owner == request.user


class IsAdminOrPaymentOwner(permissions.BasePermission):
    """
    Проверяет, связан ли пользователь с объектом Payment
    через LeaseContract и Property.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj.lease.property.owner == request.user


class IsTenantRelatedUser(permissions.BasePermission):
    """
    Проверяет, связан ли пользователь с объектом Tenant
    через LeaseContract и Property.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        lease_contracts = LeaseContract.objects.filter(tenant=obj)
        for lease in lease_contracts:
            if lease.property.owner == request.user:
                return True
        return False
