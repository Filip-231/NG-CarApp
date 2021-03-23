from rest_framework import serializers
from .models import Car, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model =Rating
        fields="Car", "rates_number","rates_sum"


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model =Car
        fields =  'id','make','model','avg_rating'

class PopularCarSerializer(serializers.ModelSerializer):
    class Meta:
        model =Car
        fields =  'id','make','model','rates_number'

