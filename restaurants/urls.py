from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, FavoriteViewSet, login_view, register_view

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
]
