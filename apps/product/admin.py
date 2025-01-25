from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'product_count']
    list_filter = ['parent']
    search_fields = ['name']
    ordering = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'old_price', 'price']
    list_filter = ['category']
    search_fields = ['name']
    inlines = [ProductImageInline]
    ordering = ['name']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
