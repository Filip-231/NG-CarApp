
from django.urls import path

from .views import CarListView, RatingListView, PopularListView, DeleteView, index, list_catalogue,help_view
urlpatterns = [
    path('', index),
    path('help/',help_view),
    path("cars/", CarListView.as_view()),
    path("cars/<int:id>/", DeleteView.as_view()),
    path("rate/", RatingListView.as_view()),
    path("popular/", PopularListView.as_view()),
    path('raw/catalogue/', list_catalogue),
]
