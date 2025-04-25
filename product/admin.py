from django.contrib import admin

from product.models import Product, Option


admin.site.register(Product)
admin.site.register(Option)
