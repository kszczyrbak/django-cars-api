from rest_framework import viewsets, mixins
from .models import Car, Rating
from .serializers import CarSerializer, CarPostSerializer, RatingSerializer, PopularCarSerializer
from .responses import bad_request_response, model_saved_response, server_error_response
from django.db.models import Avg, Value, Count
from django.db.models.functions import Coalesce
from .services import CarVPICApiService
from .filters import CarFilter, PopularCarFilter
from django.db import Error


class CarViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Car.objects.all().annotate(
        rating=Coalesce(Avg('ratings__value'), Value('0')))
    filterset_class = CarFilter

    def create(self, request, *args, **kwargs):

        car_serializer = CarPostSerializer(data=request.data)

        if not car_serializer.is_valid():
            return bad_request_response(car_serializer.errors)

        data = car_serializer.validated_data
        make, model = data['make'], data['model']
        if CarVPICApiService.validate_make_and_model(make, model):
            try:
                car = car_serializer.save()
            except Error:
                return server_error_response(CarSerializer(car).data)
            return model_saved_response(CarSerializer(car).data)

        return bad_request_response(car_serializer.errors)

    def get_serializer_class(self):
        if self.action == 'create':
            return CarPostSerializer
        return CarSerializer


class RatingViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):

        rating_serializer = RatingSerializer(data=request.data)

        if not rating_serializer.is_valid():
            return bad_request_response(rating_serializer.errors)

        data = rating_serializer.validated_data

        try:
            rating = rating_serializer.save()
        except Error:
            return server_error_response(RatingSerializer(rating).data)
        return model_saved_response(RatingSerializer(rating).data)


class PopularCarViewset(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Car.objects.all().annotate(num_ratings=Coalesce(
        Count('ratings'), Value(0))).order_by('-num_ratings')
    serializer_class = PopularCarSerializer
    filter_class = PopularCarFilter
