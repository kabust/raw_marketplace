from django.db import models


class Image(models.Model):
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255, unique=True)
    image = models.ImageField()
