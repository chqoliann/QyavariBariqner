from rest_framework.routers import DefaultRouter
from . import api_views
from django.urls import path, include


router = DefaultRouter()

router.register(r'type', api_views.TypeViewSet)
router.register(r'prouct', api_views.ProductViewSet)
router.register(r'cart', api_views.CartViewSet)
router.register(r'c_item', api_views.CartItemViewSet)
router.register(r'uprofile', api_views.UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls))
]