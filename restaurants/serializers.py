from rest_framework import serializers
from .models import Restaurants

# Serializer for Restaurant model, so that it returns JSON/XML
# If you want to serialize specific fields then change '__all__' for ('id','name','etc'...)
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = '__all__'