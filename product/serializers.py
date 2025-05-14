from rest_framework import serializers

from product.models import Product, Option, Category


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ("type", "value")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class ProductSerializer(serializers.ModelSerializer):

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

        def create(self, validated_data):
            category = validated_data.pop("category")
            options = validated_data.pop("options")
            product = super().create(validated_data)
            for option in options:
                product.options.add(option)

            category, _ = Category.objects.get_or_create(name=category)

            return product
