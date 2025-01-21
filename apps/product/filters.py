from django_filters import rest_framework as filters
from .models import Product, Category


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = filters.NumberFilter(method='filter_category')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']

    @staticmethod
    def filter_category(queryset, name, value):
        categories = [value]
        category = Category.objects.filter(id=value).first()
        if category:
            for child in category.children.all():
                categories.append(child.id)

        return queryset.filter(category_id__in=categories)
