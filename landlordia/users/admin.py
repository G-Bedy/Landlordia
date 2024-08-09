from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    )
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = (
        'email',
        'is_active',
        'is_staff',
        'is_superuser'
    )
