from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import SimpleListFilter

from apps.accounts.models import User


class RoleFilter(SimpleListFilter):
    title = 'Роль'
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        return [
            ['partner', 'партнер'],
            ['client', 'клиент']
        ]

    def queryset(self, request, queryset):
        if self.value() == 'partner':
            return queryset.filter(is_partner=True)
        if self.value() == 'client':
            return queryset.filter(is_partner=False)
        return queryset

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'is_partner', 'phone_number')
    readonly_fields = ('date_joined',)
    ordering = ('-date_joined',)
    list_filter = [RoleFilter]
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
