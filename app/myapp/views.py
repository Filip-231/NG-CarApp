from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.db.models import Count
from myapp.models import Car, Rating, Catalogue
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .decorators import has_car_payload, has_rating_payload, has_proper_rating_payload, unique_model, car_in_database
from .serializers import CarSerializer, RatingSerializer, PopularCarSerializer
import json
import requests as req


class CarListView(APIView):
    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    @has_car_payload
    @unique_model
    def post(self, make, model):
        checkincatalogue = True
        if (checkincatalogue and not check_car(make.lower(), model.lower())):
            response = [{'Error': 'Car does not exist in catalogue!'}]
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            print("Car is available in catalogue, adding to database!")
            create_car(make, model)
            response = [{"Success": "Car added successfully!"}]
            return Response(response)


class RatingListView(APIView):
    def get(self, request):
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    @has_rating_payload
    @has_proper_rating_payload
    def post(self, car_id, cur_rating):
        """Rating car with given id with integer number from 1 to 5"""

        update_rating(car_id, cur_rating)
        response = [{"Success": "Car rated!"}]
        return Response(response)


class PopularListView(APIView):
    def get(self, request, num_popular_cars=2):

        cars = Car.objects.all() \
                .annotate(num_rating=Count('rating')) \
                .order_by('-num_rating')[:num_popular_cars]

        serializer = PopularCarSerializer(cars, many=True)
        return Response(serializer.data)


class DeleteView(APIView):
    @car_in_database
    def delete(self, car):
        car.delete()
        response = [{"Success:": "Car successfuly deleted from database!"}]
        return Response(response)


def index(request):
    """Starting page"""
    return render(request, 'myapp/index.html')


def help_view(request):
    "Returning page with documentation"
    return render(request, "myapp/documentation.html")


def list_catalogue(request):
    """ List all downloaded cars from online page"""
    if request.method == 'GET':
        data = list(Catalogue.objects.values())
        return JsonResponse(data, safe=False)
    else:
        response = [{"Error": "Method not allowed"}]
        print(response)
        return JsonResponse(response, status=405, safe=False)


def create_car(make, model):
    """ Creating new car and rating object in database"""
    car = Car(make=make, model=model)
    car.save()

    return car.id


def update_rating(car_id, cur_rating):
    """ updating rating of car with id by cur_rating"""
    car = Car.objects.get(id=car_id)
    rating = Rating(Car=car, value=cur_rating)
    rating.save()


def check_car(make, model, num_attempts=5):
    """Checking in downloaded or online catalogue form page: https://vpic.nhtsa.dot.gov/api/ if car exists"""

    url = "https://vpic.nhtsa.dot.gov/api//vehicles/GetModelsForMake/{}?format=json".format(
        make)
    try:
        data = Catalogue.objects.get(make=make.lower())
        print("You checked that make already!")
        return model.lower() in data.available_models

    except:
        while True:
            try:
                print("Accessing: {}".format(url))
                resp = req.get(url)
                if resp.status_code == 200:
                    break
            except:
                print("Trying one more..")
                pass

            num_attempts = num_attempts - 1
            if (num_attempts == 0):
                return False

        models_makes = resp.json()['Results']
        models = {elem['Model_Name'].lower() for elem in models_makes}
        record = Catalogue(make=make, available_models=models)
        record.save()
        return model in models
