from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]
