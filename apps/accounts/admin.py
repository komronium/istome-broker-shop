from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'is_partner', 'phone_number')
    readonly_fields = ('date_joined',)
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': (
            'email', 'full_name', 'phone_number', 'is_partner', 'inn'
        )}),
        ('Extra information', {'fields': ('password', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'full_name', 'phone_number')
        }),
    )
