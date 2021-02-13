from .models import Car, Rating

from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):

    rating = serializers.DecimalField(
        default=0, max_digits=5, decimal_places=2)

    class Meta:
        model = Car
        fields = '__all__'


class PopularCarSerializer(serializers.ModelSerializer):

    num_ratings = serializers.IntegerField(default=0)

    class Meta:
        model = Car
        fields = '__all__'

# TODO: explicit validation?

class CarPostSerializer(serializers.Serializer):

    make = serializers.CharField(max_length=50, required=True)
    model = serializers.CharField(max_length=50, required=True)

    def create(self, validated_data):
        return Car.objects.create(**validated_data)


class RatingSerializer(serializers.Serializer):

    car = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Car.objects.all())
    value = serializers.IntegerField(required=True, min_value=1, max_value=5)

    def create(self, validated_data):
        return Rating.objects.create(**validated_data)

    class Meta:
        model = Rating
        fields = ('id', 'value', 'car')
