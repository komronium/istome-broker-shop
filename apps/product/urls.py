from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.product.views import (
    CategoryListView,
    ProductListView,
    FeaturedProductListView,
    FeatureProductView,
    ImageCreateView,
    ImageDetailView
)

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='category-list'),
    path('products', ProductListView.as_view(), name='product-list'),
    path('products/<int:product_id>/feature', FeatureProductView.as_view(), name='feature-product'),
    path('products/featured', FeaturedProductListView.as_view(), name='featured-products'),
    path('images', ImageCreateView.as_view(), name='image-create'),
    path('images/<int:image_id>/', ImageDetailView.as_view(), name='image-detail')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
