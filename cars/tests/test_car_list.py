from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from cars.models import Car, Rating
from cars.serializers import CarSerializer


class CarListTestCase(APITestCase):

    def __add_test_car(self, **kwargs):
        car = Car.objects.create(**kwargs)
        self.test_cars.append(car)
        return car

    def __add_test_rating(self, **kwargs):
        rating = Rating.objects.create(**kwargs)
        return rating

    def setUp(self):
        self.test_cars = []
        self.test_car = self.__add_test_car(make='Honda', model='Civic')
        self.__add_test_car(make='Audi', model='A4')
        self.__add_test_car(make='Honda', model='CR-V')

    def test_get_cars(self):
        """Listing cars returns proper cars"""

        response = self.client.get('/api/cars/')
        data = response.data['results']
        response_data = CarSerializer(data, many=True).data
        expected_data = CarSerializer(self.test_cars, many=True).data
        self.assertEqual(response_data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_cars_filtering_by_make(self):
        """Filtering list of cars by make returns proper cars"""
        test_make = self.test_car.make
        response = self.client.get(f'/api/cars/?make={test_make}')
        data = response.data['results']
        response_data = CarSerializer(data, many=True).data
        expected_models = [
            model for model in self.test_cars if model.make.lower() == test_make.lower()]
        expected_data = CarSerializer(expected_models, many=True).data
        self.assertEqual(response_data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_cars_filtering_by_make_case_insensitiveness(self):
        """Filtering list of cars by make is case insensitive"""

        test_make = self.test_car.make
        upper_test_make = test_make.upper()
        lower_test_make = test_make.lower()
        upper_response = self.client.get(f'/api/cars/?make={upper_test_make}')
        lower_response = self.client.get(f'/api/cars/?make={lower_test_make}')
        self.assertEqual(lower_response.data, upper_response.data)
        self.assertEqual(upper_response.status_code, 200)
        self.assertEqual(lower_response.status_code, 200)

    def test_cars_filtering_by_model(self):
        """Filtering list of cars by model returns proper cars"""

        test_model = self.test_car.model
        response = self.client.get(f'/api/cars/?model={test_model}')
        data = response.data['results']
        response_data = CarSerializer(data, many=True).data
        expected_models = [model for model in self.test_cars
                           if model.model.lower() == test_model.lower()]
        expected_data = CarSerializer(expected_models, many=True).data
        self.assertEqual(response_data, expected_data)
        self.assertEqual(response.status_code, 200)

    def test_cars_filtering_by_model_case_insensitiveness(self):
        """Filtering list of cars by model is case insensitive"""

        test_model = self.test_car.model
        upper_test_model = test_model.upper()
        lower_test_model = test_model.lower()
        upper_response = self.client.get(
            f'/api/cars/?model={upper_test_model}')
        lower_response = self.client.get(
            f'/api/cars/?model={lower_test_model}')
        self.assertEqual(lower_response.data, upper_response.data)
        self.assertEqual(upper_response.status_code, 200)
        self.assertEqual(lower_response.status_code, 200)

    def test_car_includes_rating(self):
        """Listing cars includes their proper average rating"""
        self.__add_test_rating(car=self.test_car, value=3)
        self.__add_test_rating(car=self.test_car, value=4)

        response = self.client.get(f'/api/cars/')
        data = response.data['results']

        rated_car = [serialized_car for serialized_car in data
                     if serialized_car['id'] == self.test_car.id][0]

        self.assertEqual(rated_car['rating'], '3.50')

    def test_car_rating_is_0_by_default(self):
        """Listing cars with no ratings returns 0 by default"""

        response = self.client.get('/api/cars/')
        data = response.data['results']

        self.assertEqual(data[0]['rating'], '0.00')

    def test_cars_empty_response(self):
        """Returns empty list if no cars exist in database"""

        Car.objects.all().delete()
        response = self.client.get(f'/api/cars/')
        data = response.data['results']
        self.assertEqual(data, [])
        self.assertEqual(response.status_code, 200)
