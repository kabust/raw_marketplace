from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from product.models import Product, Option, Category
from product.serializers import ProductSerializer, OptionSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("options").select_related("category")
    serializer_class = ProductSerializer


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer