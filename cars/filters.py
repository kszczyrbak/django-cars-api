from django_filters import rest_framework as filters
from .models import Car, Rating


class CarFilter(filters.FilterSet):
    make = filters.CharFilter(field_name="make", lookup_expr='iexact')
    model = filters.CharFilter(field_name="model", lookup_expr='iexact')

    ordering = filters.OrderingFilter(
        fields=(
            ('make', 'make'),
            ('model', 'model'),
            ('rating', 'rating')
        )
    )


class PopularCarFilter(filters.FilterSet):
    make = filters.CharFilter(field_name="make", lookup_expr='iexact')
