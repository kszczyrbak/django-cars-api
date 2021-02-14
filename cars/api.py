from rest_framework import viewsets, mixins
from .models import Car, Rating
from .serializers import CarSerializer, CarPostSerializer, RatingPostSerializer, PopularCarSerializer
from .responses import bad_request_response, model_saved_response, server_error_response, model_already_exists_response
from django.db.models import Avg, Value, Count
from django.db.models.functions import Coalesce
from .services import CarVPICApiService
from .filters import CarFilter, PopularCarFilter
from django.db import IntegrityError, Error
from rest_framework import filters


class CarViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Car.objects.all().annotate(
        rating=Coalesce(Avg('ratings__value'), Value('0')))
    filterset_class = CarFilter
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['make', 'model', 'rating']
    ordering = ['rating']

    def __is_in_vpic_response(self, model_name, response):
        for unit in response['Results']:
            model = unit['Model_Name']
            if model.lower() == model_name.lower():
                return True
        return False

    def create(self, request, *args, **kwargs):

        car_serializer = CarPostSerializer(data=request.data)

        if not car_serializer.is_valid():
            return bad_request_response(car_serializer.errors)

        data = car_serializer.validated_data
        make, model = data['make'], data['model']
        vpic_response = CarVPICApiService.get_models_by_make(make)
        if self.__is_in_vpic_response(model, vpic_response):
            try:
                car = car_serializer.save()
            except IntegrityError:
                return model_already_exists_response(data)
            except Error:
                return server_error_response(data)

            return model_saved_response(CarSerializer(car).data)

        return bad_request_response(car_serializer.data, car_serializer.errors)

    def get_serializer_class(self):
        if self.action == 'create':
            return CarPostSerializer
        return CarSerializer


class RatingViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = RatingPostSerializer

    def create(self, request, *args, **kwargs):

        rating_serializer = RatingPostSerializer(data=request.data)

        if not rating_serializer.is_valid():
            return bad_request_response(rating_serializer.errors)

        data = rating_serializer.validated_data

        try:
            rating = rating_serializer.save()
        except Error:
            return server_error_response(data)
        return model_saved_response(RatingPostSerializer(rating).data)


class PopularCarViewset(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Car.objects.all().annotate(num_ratings=Coalesce(
        Count('ratings'), Value(0))).order_by('-num_ratings')
    serializer_class = PopularCarSerializer
    filter_class = PopularCarFilter
