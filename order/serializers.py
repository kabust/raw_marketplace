from rest_framework import serializers

from order.models import CartEntry, Cart, PaymentMethod, Checkout


class CartEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CartEntry
        fields = (
            "id",
            "product",
            "amount",
            "entry_total",
        )
        read_only_fields = ("entry_total",)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            "id",
            "cart_entries",
        )


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = (
            "id",
            "name",
        )


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = (
            "id",
            "cart",
            "payment_method",
            "is_address_differs",
            "first_name_delivery",
            "last_name_delivery",
            "country_delivery",
            "city_delivery",
            "street_name_delivery",
            "house_number_delivery",
            "first_name_payment",
            "last_name_payment",
            "country_payment",
            "city_payment",
            "street_name_payment",
            "house_number_payment",
        )

    def validate(self, data):
        if not data.get("is_address_differs", True):
            data["first_name_payment"] = data.get("first_name_delivery")
            data["last_name_payment"] = data.get("last_name_delivery")
            data["country_payment"] = data.get("country_delivery")
            data["city_payment"] = data.get("city_delivery")
            data["street_name_payment"] = data.get("street_name_delivery")
            data["house_number_payment"] = data.get("house_number_delivery")
        return data