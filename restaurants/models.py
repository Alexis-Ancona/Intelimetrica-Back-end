from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Restaurant table schema:
# Restaurants (
#             id TEXT PRIMARY KEY, -- Unique Identifier of Restaurant
#             rating INTEGER, -- Number between 0 and 4
#             name TEXT, -- Name of the restaurant
#             site TEXT, -- Url of the restaurant
#             email TEXT,
#             phone TEXT,
#             street TEXT,
#             city TEXT,
#             state TEXT,
#             lat FLOAT, -- Latitude
#             lng FLOAT) -- Longitude


class Restaurants(models.Model):
    id = models.CharField(max_length = 50, primary_key = True, unique = True)
    rating = models.IntegerField(validators=[ # Number between 0 and 4
            MaxValueValidator(4),
            MinValueValidator(0)])
    name = models.CharField(max_length = 100) # Name of the restaurant
    site = models.CharField(max_length = 100) # Url of the restaurant
    email = models.EmailField(max_length = 100) # This field is "EmailField" instead of a text field just to make sure this entry is a valid email
    phone = models.CharField(max_length = 20)
    street = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    lat = models.FloatField() # Latitude
    lng = models.FloatField() # Longitude

# The next function return the name of the restaurant when an instance is called (if you want to return any other of the fields, just change .name for another field)
    def __str__(self):
        return self.name