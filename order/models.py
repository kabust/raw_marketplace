from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models

from product.models import Product
from user.models import User


class CartEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.SmallIntegerField(validators=[MaxValueValidator(100)])

    @property
    def entry_total(self):
        return self.product.final_price * self.amount

    def __str__(self):
        return f"{self.product}: {self.amount} pcs, {self.entry_total}"


class Cart(models.Model):
    timestamp_first_added = models.DateTimeField(auto_now=True)
    cart_entries = models.ForeignKey(CartEntry, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.cart_entries.entry_total}"



class PaymentMethod(models.Model):
    class PaymentType(models.TextChoices):
        GOOGLE = "google", "Google"
        APPLE = "apple", "Apple"
        CARD = "card", "Card"
        CASH = "cash", "Cash"

    name = models.CharField(max_length=63, choices=PaymentType.choices)

    def __str__(self):
        return self.name


class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    is_payed = models.BooleanField(default=False)
    is_address_differs = models.BooleanField(default=False)
    payment_finalized_timestamp = models.DateTimeField(null=True)
    first_name_delivery = models.CharField(max_length=63)
    last_name_delivery = models.CharField(max_length=63)
    country_delivery = models.CharField(max_length=255)
    city_delivery = models.CharField(max_length=255)
    street_name_delivery = models.CharField(max_length=255)
    house_number_delivery = models.CharField(max_length=63, blank=True, null=True)
    first_name_payment = models.CharField(max_length=63, blank=True, null=True)
    last_name_payment = models.CharField(max_length=63, blank=True, null=True)
    country_payment = models.CharField(max_length=255, blank=True, null=True)
    city_payment = models.CharField(max_length=255, blank=True, null=True)
    street_name_payment = models.CharField(max_length=255, blank=True, null=True)
    house_number_payment = models.CharField(max_length=63, blank=True, null=True)

    def __str__(self):
        return f"{self.is_payed}"



class Order(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    checkout = models.ForeignKey(Checkout, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"User {self.user.email} ordered items from cart_id: {self.cart.id}"
