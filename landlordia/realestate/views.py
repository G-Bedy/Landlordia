from django.shortcuts import render
from rest_framework import generics

from .models import *
from .serialisers import *


class OwnerAPIList(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerialiser


class OwnerAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerialiser


class PropertyAPIList(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerialiser


class PropertyAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerialiser


class TenantAPIList(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerialiser


class TenantAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerialiser


class LeaseContractAPIList(generics.ListCreateAPIView):
    queryset = LeaseContract.objects.all()
    serializer_class = LeaseContractSerialiser


class LeaseContractAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeaseContract.objects.all()
    serializer_class = LeaseContractSerialiser


class PaymentAPIList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerialiser


class PaymentAPIRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerialiser