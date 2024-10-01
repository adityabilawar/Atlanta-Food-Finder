# from django.shortcuts import render
# from rest_framework import viewsets, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import Restaurant, Favorite
# from .serializers import RestaurantSerializer, FavoriteSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
# import json
# from django.http import JsonResponse

from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Restaurant, Favorite
from .serializers import RestaurantSerializer, FavoriteSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

def landing(request):
    return render(request, "landing.html")

def about(request):
    return render(request, "about.html")

def register(request):
    return render(request, "register.html")

def forgot_password(request):
    return render(request, "forgot-password.html")

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return JsonResponse({'message': 'Please provide username, email, and password'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Username already exists'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email already exists'}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'message': 'Please provide username and password'}, status=400)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'cuisine_type', 'address']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_favorite(self, request, pk=None):
        restaurant = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
        if created:
            return Response({"message": "Added to favorites"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Already in favorites"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_favorite(self, request, pk=None):
        restaurant = self.get_object()
        favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).first()
        if favorite:
            favorite.delete()
            return Response({"message": "Removed from favorites"}, status=status.HTTP_200_OK)
        return Response({"message": "Not in favorites"}, status=status.HTTP_404_NOT_FOUND)

class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)