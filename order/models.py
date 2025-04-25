from django.db import models

from cart.models import Cart
from checkout.models import Checkout
from user.models import User


class Order(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    checkout = models.ForeignKey(Checkout, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"User {self.user.email} ordered items from cart_id: {self.cart.id}"
