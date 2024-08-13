from django.contrib import admin

from realestate.models import LeaseContract, Payment, Property, Tenant


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
            'owner',
            'address',
            'property_type',
            'description',
            'rental_type',
            'price',
            'price_period',
            'minimum_rental_value',
            'minimum_rental_unit'
        )
    search_fields = ('owner__user__username', 'address', 'property_type')
    list_filter = ('owner', 'property_type')

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address'
        )
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'address')
    list_filter = ('first_name', 'last_name', 'email')

@admin.register(LeaseContract)
class LeaseContractAdmin(admin.ModelAdmin):
    list_display = (
            'property',
            'tenant',
            'start_date',
            'end_date',
            'rent_amount',
            'rent_period',
            'deposit_amount'
        )
    search_fields = ('property__address', 'tenant__first_name', 'tenant__last_name')
    list_filter = ('property', 'tenant', 'start_date', 'end_date')
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
            'lease',
            'amount',
            'payment_date'
        )
    search_fields = ('lease_contract__property__address', 'amount')
    list_filter = ('payment_date',)
