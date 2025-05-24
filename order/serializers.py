from django.db import transaction
from rest_framework import serializers

from order.models import CartEntry, Cart, PaymentMethod, Checkout, Order
from product.models import Product
from user.utils import get_authentication_code_payu, create_order_payu, get_user_or_session_key


class CartEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CartEntry
        fields = (
            "id",
            "cart",
            "product",
            "amount",
            "entry_total",
        )
        read_only_fields = ("entry_total", "cart")

    def validate(self, attrs):
        product = attrs.get("product")
        amount = attrs.get("amount")

        if amount < 1 or amount > product.amount:
            raise serializers.ValidationError("Insufficient amount.")

        return attrs

    def create(self, validated_data):
        user, session_key = get_user_or_session_key(self.context.get("request"))
        if user:
            cart, _ = Cart.objects.get_or_create(user=user)
        elif session_key:
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        with transaction.atomic():

            amount_to_buy = validated_data.get("amount")
            product = validated_data.get("product")
            product.amount -= amount_to_buy
            product.save()
            cart_entry = CartEntry.objects.create(**validated_data, cart=cart)

        return cart_entry


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

    def create(self, validated_data):
        checkout = super().create(validated_data)
        token, exp_time = get_authentication_code_payu()
        customer_ip = self.context.get("request").META.get("REMOTE_ADDR")
        total_price = checkout.cart.total_value
        products = [
            {
                "name": entry.product.title,
                "unitPrice": str(int(entry.product.price * 100)),
                "quantity": str(entry.amount),
            }
            for entry in checkout.cart.cart_entries.all()
        ]
        buyer = {
            "email": checkout.user.email,
            "firstName": checkout.first_name_payment,
            "lastName": checkout.last_name_payment,
            "delivery": {
                "street": checkout.street_name_payment,
                "city": checkout.city_payment,
            },
        }

        order_payu = create_order_payu(token, exp_time, customer_ip, total_price, products, buyer)
        if order_payu.get("status").get("statusCode") == "SUCCESS":
            redirect_url = order_payu.get("redirectUri")
            order_id = order_payu.get("orderId")

            Order.objects.create(
                user=checkout.user,
                checkout=checkout,
                redirect_url=redirect_url,
                payu_order_id=order_id,
            )
        return checkout


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user", "checkout", "redirect_url", "payu_order_id")
        read_only_fields = ("id", "user", "checkout", "redirect_url", "payu_order_id")
