from django.urls import path, include
from rest_framework import routers

from order.views import CartEntryViewSet, CartViewSet, PaymentMethodViewSet, CheckoutViewSet

router = routers.DefaultRouter()
router.register("cart-entries", CartEntryViewSet)
router.register("carts", CartViewSet)
router.register("payment_methods", PaymentMethodViewSet)
router.register("checkouts", CheckoutViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "order"
