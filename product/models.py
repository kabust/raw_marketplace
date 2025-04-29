import os
import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class GenderChoice(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    UNISEX = "unisex", "Unisex"


def movie_image_file_path(instance, title):
    _, extension = os.path.splitext(title)
    title = f"{slugify(instance.filename)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/products/", title)

class Image(models.Model):
    filename = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=movie_image_file_path)

    def __str__(self):
        return self.filename



class Option(models.Model):
    class OptionType(models.TextChoices):
        COLOR = "color", "Color"
        CLOTHING_SIZE = "clothing_size", "Clothing size"
        PRODUCT_SIZE = "product_size", "Product size"
        MATERIAL = "material", "Material"

    type = models.CharField(max_length=15, choices=OptionType.choices)
    value = models.CharField(max_length=63)

    def __str__(self):
        return f"{self.type}: {self.value}"


class Category(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

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
    images = models.ManyToManyField(Image, related_name="products", null=True, blank=True)
    options = models.ManyToManyField(Option, related_name="products", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    gender = models.CharField(max_length=10, choices=GenderChoice, default=GenderChoice.UNISEX)

    @property
    def final_price(self):
        return self.price * ((100 - self.discount) / 100)

    def __str__(self):
        return f"{self.title} ({self.category.name}), {self.amount} pcs in stock"
