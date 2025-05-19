from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from order.models import Checkout, CartEntry, Cart, PaymentMethod, Order
from order.serializers import (
    CartEntrySerializer,
    CartSerializer,
    CheckoutSerializer,
    PaymentMethodSerializer, OrderSerializer,
)


class CartEntryViewSet(viewsets.ModelViewSet):
    queryset = CartEntry.objects.all()
    serializer_class = CartEntrySerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
