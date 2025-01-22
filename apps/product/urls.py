from django.urls import path
from apps.product.views import (
    CategoryListView,
    ProductListView,
    FeaturedProductListView,
    FeatureProductView
)

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='category-list'),
    path('products', ProductListView.as_view(), name='product-list'),
    path('products/<int:product_id>/feature', FeatureProductView.as_view(), name='feature-product'),
    path('products/featured', FeaturedProductListView.as_view(), name='featured-products')
]
