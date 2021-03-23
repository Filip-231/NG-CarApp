from django.db import models


class Car(models.Model):
    """ Car model with make and model"""
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        unique_together = ('make', 'model',)

    @property
    def avg_rating(self):
        """Counting average rating value for specific car"""

        rating=self.rating_set.first()#I take first  kind of rating
        avg_rating = 0.0
        if(rating.rates_number > 0):
            avg_rating = round(rating.rates_sum/rating.rates_number, 1)
        return(avg_rating)
    
    @property
    def rates_number(self):
        return self.rating_set.first().rates_number


class Rating(models.Model):
    """ Model containing rating for each car
    I decided to make many to one relation, because after scalling up the application,
    each car can get more kinds of ratings, 
    for example online rating, customer rating, production rating """
    Car= models.ForeignKey(Car, blank=True, null=True,
                            on_delete=models.CASCADE)
    # car_parent=models.OneToOneField(
    #     Car,
    #     on_delete=models.CASCADE,
    #     primary_key=True,
    # )

    rates_number = models.IntegerField(blank=True, null=True)
    rates_sum = models.IntegerField(blank=True, null=True)


class Catalogue(models.Model):
    """ 
    When I checked one time available models for make in online catalogue,
    I write it to database,
    to get faster access next time when checking the same model
    """
    make = models.CharField(max_length=100)
    available_models = models.CharField(max_length=1000)
