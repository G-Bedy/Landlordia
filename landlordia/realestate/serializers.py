from realestate.models import LeaseContract, Owner, Payment, Property, Tenant
from rest_framework import serializers


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = [
            'user',
            'phone_number',
            'address'
        ]


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'owner',
            'address',
            'property_type',
            'description',
            'rental_type',
            'price',
            'price_period',
            'minimum_rental_value',
            'minimum_rental_unit'
        ]


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address'
        ]


class LeaseContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaseContract
        fields = [
            'property',
            'tenant',
            'start_date',
            'end_date',
            'rent_amount',
            'rent_period',
            'deposit_amount'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'lease',
            'amount',
            'payment_date'
        ]
