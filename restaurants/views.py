from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from geopy import distance
import statistics as estadistica

from .models import Restaurants
from .serializers import RestaurantSerializer
# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
def RestaurantList(request):
    try: restaurants = Restaurants.objects.all()
    except Restaurants.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)

    #restaurants/ GET   retrieves a list with all restaurants in DB
    if request.method == 'GET':
        serializer = RestaurantSerializer(restaurants, many = True)
        return Response(serializer.data)

    #restaurants/ POST  Creates a restaurant
    elif request.method == 'POST':
        serializer = RestaurantSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    #restaurants/ DELETE  Deletes all restaurants in DB
    elif request.method == 'DELETE':
        restaurants.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def RestaurantID(request, pk):
    try: restaurant = Restaurants.objects.get(id = pk)
    except Restaurants.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)

    #restaurants/id GET  Shows a restaurant according to id
    if request.method == 'GET':
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)
    
    #restaurants/id PUT    modifies a restaurant according to id
    elif request.method == 'PUT':
        serializer = RestaurantSerializer(restaurant, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    #restaurants/id DELETE   deletes a restaurant according to id
    elif request.method == 'DELETE':
        restaurant.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


#EXAMPLE: ?latitude=19.4423123&longitude=-99.12712398&radius=600
@api_view(['GET'])
def statistics(request):
    latitude = float(request.GET.get('latitude'))
    longitude = float(request.GET.get('longitude'))
    radius = float(request.GET.get('radius'))
    restaurantList = Restaurants.objects.all()
    distancias = []
    ratings = []
    count = 0
    avg = 0
    std = 0
    acum = 0
    for restaurant in restaurantList:
        rest1C = (latitude,longitude)
        rest2C = (restaurant.lat, restaurant.lng)
        distancia = distance.distance(rest1C, rest2C).m
        distancias.append(distancia)
        if distancia <= radius:
            count += 1
            acum = acum + restaurant.rating
            avg = acum / count
            ratings.append(restaurant.rating)
        if count > 1 :
            std = estadistica.stdev(ratings)
    
    ctx = {
            "count": count,
            "avg": avg,
            "std": std
            }
    return Response(ctx)


# JSON EXAMPLE
# {
#     "id" : "8",
#     "rating": 3,
#     "name": "This field is required.",
#     "site": "This field is required.",
#     "email": "a@a.com",
#     "phone": "2190387462",
#     "street": "This field is required.",
#     "city": "This field is required.",
#     "state": "This field is required.",
#     "lat": 123.23,
#     "lng": -23.123
# }