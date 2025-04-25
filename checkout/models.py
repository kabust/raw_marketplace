from django.db import models

from cart.models import Cart
from user.models import User


class PaymentMethod(models.Model):
    name = models.CharField(max_length=63, unique=True)


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
