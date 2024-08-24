from rest_framework import serializers

from realestate.models import LeaseContract, Payment, Property, Tenant


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
        read_only_fields = ['owner', ]


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
            'deposit_amount',
            'next_payment_date',
        ]

    read_only_fields = ['next_payment_date']

    def validate(self, data):
        """Проверка дат начала и окончания аренды."""
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError(
                "Дата окончания аренды не может быть раньше даты начала аренды"
            )
        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'lease',
            'amount',
            'payment_date'
        ]
