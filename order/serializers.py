from rest_framework import serializers

from order.models import CartEntry, Cart, PaymentMethod, Checkout, Order
from user.utils import get_authentication_code_payu, create_order_payu


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
