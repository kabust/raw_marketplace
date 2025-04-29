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
    main_image = ImageSerializer(write_only=True)

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
            "images",
            "options",
            "category",
            "gender",
            "main_image",
        )

    def create(self, validated_data):
        images_data = validated_data.pop("main_image")

        image = Image.objects.create(**images_data)
        product = Product.objects.create(main_image=image, **validated_data)

        return product


class ProductListSerializer(ProductSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    main_image = serializers.CharField(source="main_image.filename", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "price",
            "discount",
            "final_price",
            "is_active",
            "main_image",
            "category",
            "gender",
        )

class ProductDetailSerializer(ProductSerializer):
    options = OptionSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)
    main_image = serializers.CharField(source="main_image.filename", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "price",
            "discount",
            "final_price",
            "description",
            "amount",
            "is_active",
            "main_image",
            "images",
            "options",
            "category",
            "gender",
        )


