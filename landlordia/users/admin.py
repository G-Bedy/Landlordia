from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'name',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    )
    search_fields = ('email',)
    list_filter = ('email',)
