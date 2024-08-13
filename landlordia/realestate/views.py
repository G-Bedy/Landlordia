from realestate.models import LeaseContract, Payment, Property, Tenant
from realestate.permissions import IsAdminOrOwner
from realestate.serializers import (LeaseContractSerializer,
                                    PaymentSerializer, PropertySerializer,
                                    TenantSerializer)
from rest_framework import generics


class PropertyAPIList(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAdminOrOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Property.objects.all()
        return Property.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # ??? спросить: нужно ли прописывать этот метод если поле owner в read_only?


class PropertyAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAdminOrOwner, ]


    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Property.objects.all()
        return Property.objects.filter(owner=self.request.user)


class TenantAPIList(generics.ListCreateAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsAdminOrOwner, ]
    # ??? спросить: нужно ли здесь и далее ниже по коду
    # указывать permission_classes = [IsAdminOrOwner, ]
    # если я прописываю get_queryset?

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Tenant.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        leases = LeaseContract.objects.filter(property__in=properties)
        return Tenant.objects.filter(leasecontract__in=leases).distinct()


class TenantAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsAdminOrOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Tenant.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        leases = LeaseContract.objects.filter(property__in=properties)
        return Tenant.objects.filter(leasecontract__in=leases).distinct()


class LeaseContractAPIList(generics.ListCreateAPIView):
    serializer_class = LeaseContractSerializer
    permission_classes = [IsAdminOrOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return LeaseContract.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        return LeaseContract.objects.filter(property__in=properties)


class LeaseContractAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeaseContractSerializer
    permission_classes = [IsAdminOrOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return LeaseContract.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        return LeaseContract.objects.filter(property__in=properties)


class PaymentAPIList(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Payment.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        leases = LeaseContract.objects.filter(property__in=properties)
        return Payment.objects.filter(lease__in=leases)


class PaymentAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrOwner, ]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Payment.objects.all()

        properties = Property.objects.filter(owner=self.request.user)
        leases = LeaseContract.objects.filter(property__in=properties)
        return Payment.objects.filter(lease__in=leases)
