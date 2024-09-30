from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Restaurant, Favorite
from .serializers import RestaurantSerializer, FavoriteSerializer

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
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'message': 'User created successfully'}, status=201)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'cuisine_type', 'address']

    @action(detail=True, methods=['post'])
    def add_favorite(self, request, pk=None):
        restaurant = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
        if created:
            return Response({"message": "Added to favorites"}, status=201)
        return Response({"message": "Already in favorites"}, status=200)

    @action(detail=True, methods=['post'])
    def remove_favorite(self, request, pk=None):
        restaurant = self.get_object()
        favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).first()
        if favorite:
            favorite.delete()
            return Response({"message": "Removed from favorites"}, status=200)
        return Response({"message": "Not in favorites"}, status=404)

class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
