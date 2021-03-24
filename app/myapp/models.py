from django.db import models
from django.db.models import Sum, Avg

class Car(models.Model):
    """ Car model with make and model"""
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        unique_together = ('make', 'model',)

    @property
    def avg_rating(self):
        """Counting average rating value for specific car"""     
        if(self.rating_set.all()):
            avg_rating=self.rating_set.all().aggregate(Avg('value'))['value__avg']
            return round(avg_rating,1)
        else: return 0.0


    @property
    def rates_number(self):
        if(self.rating_set.all()):
            return self.rating_set.all().count()
        else: return 0

class Rating(models.Model):
    """ Model containing rating for each car
    I decided to make many to one relation, because after scalling up the application,
    each car can get more kinds of ratings, for example from different users """
    Car = models.ForeignKey(Car, blank=True, null=True,
                            on_delete=models.CASCADE)
    value = models.IntegerField(blank=True, null=True)


class Catalogue(models.Model):
    """ 
    When I checked one time available models for make in online catalogue,
    I write it to database,
    to get faster access next time when checking the same model
    """
    make = models.CharField(max_length=100)
    available_models = models.CharField(max_length=1000)
