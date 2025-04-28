from django.contrib import admin

from order.models import Order, PaymentMethod, Checkout

admin.site.register(Order)
admin.site.register(Checkout)
admin.site.register(PaymentMethod)