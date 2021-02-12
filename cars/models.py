from django.db import models

# Create your models here.


class Car(models.Model):

    make = models.CharField(max_length=50)

    model = models.CharField(max_length=50)


class Rating(models.Model):

    value = models.IntegerField()

    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='ratings')
