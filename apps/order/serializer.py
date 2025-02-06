from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone', 'city', 'street', 'house', 'apartment',
            'comment', 'total_price', 'items', 'created_at'
        ]

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity']
            )

        return order
