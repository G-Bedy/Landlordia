from rest_framework import serializers

from .models import *


class OwnerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class PropertySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class TenantSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'


class LeaseContractSerialiser(serializers.ModelSerializer):
    class Meta:
        model = LeaseContract
        fields = '__all__'


class PaymentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'