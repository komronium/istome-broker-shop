from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Category, Product, ProductImage, FeaturedProduct


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count', 'children']

    @staticmethod
    def get_children(obj):
        return CategorySerializer(obj.children.all(), many=True).data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    is_featured = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category', 'price', 'old_price', 'quantity', 'is_featured', 'images']

    def get_category(self, obj):
        return {
            'id': obj.category.id,
            'name': obj.category.name
        }

    def get_is_featured(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and FeaturedProduct.objects.filter(user=user, product=obj).exists()


class FeatureProductSerializer(serializers.Serializer):

    def create(self, validated_data):
        product = get_object_or_404(Product, id=validated_data.get('product_id'))
        featured_product, created = FeaturedProduct.objects.get_or_create(
            user=validated_data.get('user'),
            product=product
        )
        if not created:
            featured_product.delete()

        return ProductSerializer(product, context=self.context).data
