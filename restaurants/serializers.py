from rest_framework import serializers
from .models import Restaurant, Favorite

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'cuisine_type', 'rating']

class FavoriteSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'restaurant']