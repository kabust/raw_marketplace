from rest_framework import serializers

from product.models import Product, Option, Category, Image


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ("type", "value")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("filename", "image")



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class ProductSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)
    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "price",
            "discount",
            "description",
            "amount",
            "is_active",
            "main_image",
            "images",
            "options",
            "category",
            "gender",
        )

