import json
from django.shortcuts import render
from myapp.models import Car, Rating, Catalogue
from rest_framework.response import Response
from rest_framework import status



def has_car_payload(func):
    def check_payload(view, request):
        try:
            payload = json.loads(request.body)
            make,model = payload['make'],payload['model']
            return func(view, make,model)
        except:
            response = [{"Error": "Car could not be added! Wrong payload!"}]
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    return check_payload


def unique_model(func):
    def check_unique(view, make,model):
        try:
            Car.objects.get(make__iexact=make, model__iexact=model)
            response = [{"Error": "Car is already in database!"}]
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            return func(view, make,model)

    return check_unique

def has_rating_payload(func):
    def check_payload(view, request):
        try:
            payload = json.loads(request.body)
            car_id,cur_rating = payload['car_id'],payload['rating']
            return func(view, car_id,cur_rating)
        except:
            response = [{"Error": "Rating could not be added! Wrong payload!"}]
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    return check_payload

def has_proper_rating_payload(func):
    def check_rating(view,car_id,cur_rating):
        if not (type(cur_rating) == int and cur_rating >= 1 and cur_rating <= 5):
            response = [
                {"Error": "Rating must integer bigger than 1 and smaller than 5!"}]
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        else:
            return func(view,car_id,cur_rating)

    return check_rating


def car_in_database(func):
    def check_car_in_database(view,request,id):
            try:
                car = Car.objects.get(id=id)
                return func(view,car)
            except:
                response = [{'Error': 'No car with that ID'}]
                return Response(response,status=status.HTTP_400_BAD_REQUEST)

    return check_car_in_database

# BASE_ERROR_MESSAGE = 'Could not connect to your box because {error_reason}'

# def handle_view_exception(func):
#     """Decorator for handling exceptions."""
#     @functools.wraps(func)
#     def wrapper(request):
#         try:
#             #response = func(request, *args, **kwargs)

#             payload = json.loads(request.body)
#             car_id = payload['car_id']
#             cur_rating = payload['rating']
#             response=func(request)
#         except RequestException as e:
#             response = [{'Error': 'Car could not be rated!'}]
#             return Response(response,status=status.HTTP_400_BAD_REQUEST)
#         return response

#     return wrapper

# from django.contrib.auth.decorators import user_passes_test

# def teacher_required(function=None):
#     def is_teacher(u):
#         return False
#     actual_decorator = user_passes_test(is_teacher)
#     if function:
#         return actual_decorator(function)
#     else:
#         return actual_decorator

# class WrongType(Exception):
#     pass

# @dataclass
# class ExceptionHandler:
#     e: Exception
#     @staticmethod
#     def context_wrapper(code) -> dict:
#         return {'error_code': code}
# def get_error_response(self) -> Response:
#         if False:#self.e.__class__ == WrongType:
#             data = self.context_wrapper(101)
#         else:
#             data = self.context_wrapper(999)
#         return Response(data, status=status.HTTP_200_OK

# def exception(function):
#     @wraps(function)
#     def wrapper(*args, **kwargs):
#         try:
#             return function(*args, **kwargs)
#         except Exception as e:
#             return ExceptionHandler(e).get_error_response()
#     return wrapper

# @teacher_required
# def teacher_view(request):
#     # ...
#     pass

#from .decorators import handle_view_exception,teacher_required,