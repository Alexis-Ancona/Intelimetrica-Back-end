from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Restaurants
from .serializers import RestaurantSerializer
# Create your views here.

@api_view(['GET'])
def RestaurantList(request):
    restaurant_list = Restaurants.objects.all()
    serializer = RestaurantSerializer(restaurant_list, many = True)
    return Response (serializer.data)

@api_view(['GET'])
def RestaurantDetail(request, pk):
    restaurant = Restaurants.objects.get(id = pk)
    serializer = RestaurantSerializer(restaurant, many = False)
    return Response (serializer.data)


# This returns a status 200 even when a repeated id comes in (doesn't save it in the DB tho), remember to change it so it returns some error
@api_view(['POST'])
def RestaurantCreate(request):
    serializer = RestaurantSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
    return Response (serializer.data)

#This also returns a status 200 even when the rating is modified out of the (0-4) range
@api_view(['POST'])
def RestaurantUpdate(request, pk):
    restaurant = Restaurants.objects.get(id=pk)
    serializer = RestaurantSerializer(instance=restaurant, data = request.data)

    if serializer.is_valid():
        serializer.save()
    return Response (serializer.data)

@api_view(['DELETE'])
def RestaurantDelete(request, pk):
    restaurant = Restaurants.objects.get(id=pk)
    restaurant.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)