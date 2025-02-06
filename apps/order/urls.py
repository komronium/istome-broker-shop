from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.order.views import (
    OrderCreateView
)

urlpatterns = [
    path('orders', OrderCreateView.as_view(), name='order-create'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
