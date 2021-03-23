from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Restaurants
from .serializers import RestaurantSerializer
# Create your views here.

@api_view(['GET'])
def RestaurantList(request):
    restaurant_list = Restaurants.objects.all()
    serializer = RestaurantSerializer(restaurant_list, many = True)
    return Response (serializer.data)