from itertools import product

from django.db import models
from django.core.validators import MaxValueValidator

from product.models import Product


class CartEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.SmallIntegerField(validators=[MaxValueValidator(100)])

    @property
    def entry_total(self):
        return self.product.final_price * self.amount


class Cart(models.Model):
    timestamp_first_added = models.DateTimeField(auto_now=True)
    cart_entries = models.ForeignKey(CartEntry, on_delete=models.DO_NOTHING)
