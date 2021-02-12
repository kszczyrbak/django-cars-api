from rest_framework import viewsets, mixins
from .models import Car, Rating
from .serializers import CarSerializer, CarPostSerializer, RatingSerializer
from .responses import bad_request_response, car_saved_response
from .services import validate_make_and_model
from django.db.models import Avg, Value
from django.db.models.functions import Coalesce


class CarViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Car.objects.all().annotate(
        rating=Coalesce(Avg('ratings__value'), Value('0')))
    serializer_class = CarSerializer

    def create(self, request, *args, **kwargs):

        car_serializer = CarPostSerializer(data=request.data)

        if not car_serializer.is_valid():
            return bad_request_response(car_serializer.errors)

        data = car_serializer.validated_data
        make, model = data['make'], data['model']
        if validate_make_and_model(make, model):
            car = car_serializer.save()
            return car_saved_response(CarSerializer(car).data)

        return bad_request_response(car_serializer.errors)


class RatingViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = RatingSerializer

#TODO: top cars viewset