from django.contrib import admin
from .models import *

admin.site.register(Owner)
admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(LeaseContract)
admin.site.register(Payment)
