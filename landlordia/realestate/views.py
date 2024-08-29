from rest_framework import generics

from realestate.models import LeaseContract, Payment, Property, Tenant
from realestate.permissions import (IsAdminOrLeaseContractOwner,
                                    IsAdminOrOwner, IsAdminOrPaymentOwner,
                                    IsTenantRelatedUser)
from realestate.serializers import (LeaseContractSerializer, PaymentSerializer,
                                    PropertySerializer, TenantSerializer)

from .tasks import send_contract_email


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
        if self.request.user and self.request.user.is_staff:
            return Tenant.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        leases = LeaseContract.objects.filter(property__in=properties)
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
