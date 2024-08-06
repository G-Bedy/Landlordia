from realestate.models import LeaseContract, Owner, Payment, Property, Tenant
from realestate.serialisers import (LeaseContractSerializer, OwnerSerializer,
                                    PaymentSerializer, PropertySerializer,
                                    TenantSerializer)
from rest_framework import generics


class OwnerAPIList(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class OwnerAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class PropertyAPIList(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class PropertyAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class TenantAPIList(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


class TenantAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


class LeaseContractAPIList(generics.ListCreateAPIView):
    queryset = LeaseContract.objects.all()
    serializer_class = LeaseContractSerializer


class LeaseContractAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeaseContract.objects.all()
    serializer_class = LeaseContractSerializer


class PaymentAPIList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
