from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics

from realestate.models import LeaseContract, Payment, Property, Tenant
from realestate.permissions import (IsAdminOrLeaseContractOwner,
                                    IsAdminOrOwner, IsAdminOrPaymentOwner,
                                    IsTenantRelatedUser)
from realestate.serializers import (LeaseContractSerializer, PaymentSerializer,
                                    PropertySerializer, TenantSerializer)

from .tasks import send_contract_email


@method_decorator(cache_page(60*15), name='dispatch')
class PropertyAPIList(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAdminOrOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Property.objects.all()
        return Property.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAdminOrOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Property.objects.all()
        return Property.objects.filter(owner=self.request.user)


class TenantAPIList(generics.ListCreateAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsTenantRelatedUser, ]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_staff:
            return Tenant.objects.all()

        properties_cache_key = f"properties_{user.id}"
        leases_cache_key = f"leases_{user.id}"
        cache_timeout = 60 * 15
        properties = cache.get(properties_cache_key)
        leases = cache.get(leases_cache_key)

        if not properties:
            properties = Property.objects.filter(owner=user)
            cache.set(properties_cache_key, properties, cache_timeout)
        if not leases:
            leases = LeaseContract.objects.filter(property__in=properties)
            cache.set(leases_cache_key, leases, cache_timeout)
        return Tenant.objects.filter(leasecontract__in=leases).distinct()


class TenantAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsTenantRelatedUser, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Tenant.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        leases = LeaseContract.objects.filter(property__in=properties)
        return Tenant.objects.filter(leasecontract__in=leases).distinct()


class LeaseContractAPIList(generics.ListCreateAPIView):
    serializer_class = LeaseContractSerializer
    permission_classes = [IsAdminOrLeaseContractOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return LeaseContract.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        return LeaseContract.objects.filter(property__in=properties)

    def perform_create(self, serializer):
        lease_contract = serializer.save()
        tenant_email = lease_contract.tenant.email
        contract_details = str(lease_contract)
        send_contract_email.delay(tenant_email, contract_details)


class LeaseContractAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeaseContractSerializer
    permission_classes = [IsAdminOrLeaseContractOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return LeaseContract.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        return LeaseContract.objects.filter(property__in=properties)


class PaymentAPIList(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrPaymentOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Payment.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        leases = LeaseContract.objects.filter(property__in=properties)
        return Payment.objects.filter(lease__in=leases)


class PaymentAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrPaymentOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Payment.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        leases = LeaseContract.objects.filter(property__in=properties)
        return Payment.objects.filter(lease__in=leases)
