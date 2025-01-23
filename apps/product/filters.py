from django_filters import rest_framework as filters
from django.core.cache import cache

from .models import Product, Category


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = filters.NumberFilter(method='filter_category')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']

    def get_category_children(self, category_id):
        cache_key = f'category_children_ids_{category_id}'
        children_ids = cache.get(cache_key)
        
        if children_ids is None:
            category = Category.objects.filter(id=category_id).first()
            if not category:
                return []
                
            children_ids = [category_id]
            for child in category.children.all():
                children_ids.extend(self.get_category_children(child.id))
                
            cache.set(cache_key, children_ids, timeout=3600)
            
        return children_ids

    def filter_category(self, queryset, name, value):
        category_ids = self.get_category_children(value)
        return queryset.filter(category_id__in=category_ids)
