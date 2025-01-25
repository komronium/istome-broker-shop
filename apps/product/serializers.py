from django.shortcuts import get_object_or_404
from django.core.cache import cache

from rest_framework import serializers

from .models import Category, Product, ProductImage, FeaturedProduct


class ProductImageSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product_id']
        read_only_fields = ['id']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id', None)
        image = ProductImage(**validated_data)

        if product_id:
            product = get_object_or_404(Product, id=product_id)
            image.product = product

        image.save()
        return image


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count', 'children']

    @staticmethod
    def get_children(obj):
        cache_key = f'category_children_{obj.id}'
        children = cache.get(cache_key)

        if not children:
            children = CategorySerializer(obj.children.all(), many=True).data
            cache.set(cache_key, children, timeout=3600)

        return children


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    category_id = serializers.IntegerField(write_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    is_featured = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    image_ids = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_id', 'description', 'attrs', 'sku', 'category',
            'price', 'old_price', 'quantity', 'is_featured', 'like_count', 'image_ids', 'images'
        ]


    def get_category(self, obj):
        return {
            'id': obj.category.id,
            'name': obj.category.name
        } if obj.category else None

    def get_is_featured(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and FeaturedProduct.objects.filter(user=user, product=obj).exists()

    @staticmethod
    def get_like_count(obj) -> int:
        return FeaturedProduct.objects.filter(product=obj).count()

    def create(self, validated_data):
        image_ids = validated_data.pop('image_ids', [])
        category = get_object_or_404(Category, id=validated_data.pop('category_id'))
        product = Product.objects.create(**validated_data, category=category)

        for image_id in image_ids:
            image = ProductImage.objects.filter(id=image_id).first()

            if image:
                image.product = product
                image.save()

        return product



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
