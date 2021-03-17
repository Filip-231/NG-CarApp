
from django.urls import path

from .views import index, add_car, get_car, list_cars, delete_car, rate_car, list_ratings, get_popular, list_catalogue,help_view


urlpatterns = [
    path('', index),
    path('cars/', add_car),
    path('cars/<int:id>', get_car),
    path('listcars/', list_cars),
    path('cars/<int:id>/', delete_car),
    path('rate/', rate_car),
    path('ratings/', list_ratings),
    path('popular/', get_popular),
    path('catalogue/', list_catalogue),
    path('help/',help_view)
]
