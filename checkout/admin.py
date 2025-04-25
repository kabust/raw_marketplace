from django.contrib import admin

from checkout.models import Checkout, PaymentMethod


admin.site.register(Checkout)
admin.site.register(PaymentMethod)
