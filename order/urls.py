from django.urls import path, include
from rest_framework import routers

from order.views import CartEntryViewSet, CartViewSet, PaymentMethodViewSet, CheckoutViewSet

router = routers.DefaultRouter()
router.register("cart-entry", CartEntryViewSet)
router.register("cart", CartViewSet)
router.register("payment_method", PaymentMethodViewSet)
router.register("billing", CheckoutViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "order"
