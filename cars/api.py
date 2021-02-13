from rest_framework import viewsets, mixins
from .models import Car, Rating
from .serializers import CarSerializer, CarPostSerializer, RatingSerializer, PopularCarSerializer
from .responses import bad_request_response, car_saved_response
from django.db.models import Avg, Value, Count
from django.db.models.functions import Coalesce
from .services import CarVPICApiService
from .filters import CarFilter, PopularCarFilter


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
            car = car_serializer.save()
            return car_saved_response(CarSerializer(car).data)

        return bad_request_response(car_serializer.errors)

    def get_serializer_class(self):
        if self.action == 'create':
            return CarPostSerializer
        return CarSerializer


class RatingViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = RatingSerializer


class PopularCarViewset(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Car.objects.all().annotate(num_ratings=Coalesce(
        Count('ratings'), Value(0))).order_by('-num_ratings')
    serializer_class = PopularCarSerializer
    filter_class = PopularCarFilter
