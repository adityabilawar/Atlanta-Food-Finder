from django.contrib import admin
from django.urls import path, include

from restaurants import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('restaurants.urls')),
    path('api/users/', include('users.urls')),
    path('', views.landing),
    path('register/', views.register),
    path('forgot-password/', views.forgot_password)
]