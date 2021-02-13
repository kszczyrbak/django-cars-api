from django.db import models

# Create your models here.


class Car(models.Model):

    make = models.CharField(max_length=50, blank=False)

    model = models.CharField(max_length=50, unique=True, blank=False)


class Rating(models.Model):

    value = models.IntegerField(blank=False)

    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='ratings', blank=False)
