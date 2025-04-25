from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=63, unique=True)
    is_for_male = models.BooleanField(default=False)
    is_for_female = models.BooleanField(default=False)
