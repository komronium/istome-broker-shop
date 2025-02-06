from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.order.serializer import OrderSerializer


class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
