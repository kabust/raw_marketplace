from rest_framework import viewsets, status

from product.models import Product, Option, Category, Image
from product.permissions import IsAdminOrReadOnly
from product.serializers import (
    ProductSerializer,
    OptionSerializer,
    CategorySerializer,
    ImageSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("options", "images").select_related(
        "category", "main_image"
    )
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer

        if self.action == "retrieve":
            return ProductDetailSerializer

        return ProductSerializer


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = (IsAdminOrReadOnly,)
