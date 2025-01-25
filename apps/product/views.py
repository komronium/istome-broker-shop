from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductSerializer, FeatureProductSerializer, ProductImageSerializer
from .filters import ProductFilter
from ..accounts.permissions import IsPartner


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        return Category.objects.filter(parent=None)


class ProductListView(ListCreateAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'rating']

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsPartner()]


class FeaturedProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Product.objects.filter(featured_product__user=self.request.user)


class FeatureProductView(CreateAPIView):
    serializer_class = FeatureProductSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save(user=request.user, **kwargs)
        return Response(data, status=status.HTTP_200_OK)


class ImageCreateView(CreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = (IsAuthenticated,)


class ImageDetailView(RetrieveDestroyAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'image_id'

    def get_queryset(self):
        return ProductImage.objects.all()
