from django.contrib import admin

from realestate.models import LeaseContract, Owner, Payment, Property, Tenant


admin.site.register(Owner)
admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(LeaseContract)
admin.site.register(Payment)

