from django.urls import path, include
from rest_framework import routers

from product.views import ProductViewSet, OptionViewSet, CategoryViewSet, ImageViewSet

router = routers.DefaultRouter()
router.register("options", OptionViewSet)
router.register("images", ImageViewSet)
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "product"
