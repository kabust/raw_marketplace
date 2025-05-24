from django.contrib import admin

from product.models import Product, Option, Category, Image

admin.site.register(Product)
admin.site.register(Option)
admin.site.register(Image)
admin.site.register(Category)
