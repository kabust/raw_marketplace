from django.urls import path, include
from rest_framework import routers

from product.views import ProductViewSet, OptionViewSet, CategoryViewSet, ImageViewSet

router = routers.DefaultRouter()
router.register("option", OptionViewSet)
router.register("image", ImageViewSet)
router.register("product", ProductViewSet)
router.register("category", CategoryViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "product"
