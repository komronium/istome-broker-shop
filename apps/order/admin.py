from django.contrib import admin
from .models import Order, OrderItem


class ItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'total_price', 'created_at']
    search_fields = ['full_name', 'email']
    inlines = [ItemInline]
    ordering = ['-created_at']
