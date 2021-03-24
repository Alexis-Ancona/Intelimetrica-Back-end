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
    if request.method == 'GET':
        try:
            # Get latitude, longitude and radius from Url
            latitude = float(request.GET.get('latitude'))
            longitude = float(request.GET.get('longitude'))
            radius = float(request.GET.get('radius'))
        except: return Response(status = status.HTTP_400_BAD_REQUEST)
        # Make a list of restaurants so we can iterate through all objects in the DB
        restaurantList = Restaurants.objects.all()
        # Creates a list of ratings so we can pass this list as a parameter to stdev function
        ratings = []
        count = 0
        avg = 0
        std = 0
        acum = 0
        #Iterate through all objects
        for restaurant in restaurantList:
            rest1C = (latitude,longitude)
            rest2C = (restaurant.lat, restaurant.lng)
            # distance function recieves as parameters a copule of coordinates, lat and lng of point 1 and point 2 and calculates the geographical distance between them
            distancia = distance.distance(rest1C, rest2C).m
            # If the distance is less than the radius it means the restaurant is inside this "virtual circle", so we add a 1 to count and calculate the average
            if distancia <= radius:
                count += 1
                acum = acum + restaurant.rating
                avg = acum / count
                ratings.append(restaurant.rating)
            # We have to specify that "if count is grater than 1" because stdev function needs at least 2 values to work
            if count > 1 :
                std = estadistica.stdev(ratings)
        
        ctx = {
                "count": count, # Count of restaurants that fall inside the circle with center [x,y] y radius z,
                "avg": avg,     # Average rating of restaurant inside the circle,
                "std": std      # Standard deviation of rating of restaurants inside the circle
                }
        return Response(ctx)
    return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)


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