from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from category.models import Category
from image.models import Image


class Option(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(0.0)]
    )
    discount = models.PositiveSmallIntegerField(
        blank=True, null=True, default=0, validators=[MaxValueValidator(100)]
    )
    description = models.TextField(max_length=2000, blank=True, null=True)
    amount = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    main_image = models.OneToOneField(
        Image,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="product_main"
    )
    images = models.ManyToManyField(Image, related_name="products")
    options = models.ManyToManyField(Option, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    @property
    def final_price(self):
        return self.price * ((100 - self.discount) / 100)

    def __str__(self):
        return f"{self.title} ({self.category.name}), {self.amount} pcs in stock"
