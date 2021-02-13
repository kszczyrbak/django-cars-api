from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from cars.models import Car
from cars.serializers import CarPostSerializer
from unittest.mock import Mock, patch
from .mocks import mock_model_doesnt_exist, mock_model_exists
import random
import string


@patch('cars.services.requests.get')
class CarCreateTestCase(APITestCase):

    def __add_test_car(self, **kwargs):
        car = Car.objects.create(**kwargs)
        self.test_cars.append(car)
        return car

    def __generate_random_string(self, length):
        return ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(length))

    def setUp(self):
        self.test_cars = []
        self.test_ratings = []
        self.test_make = "Honda"
        self.test_model = "Civic"

        self.test_car_post_body = {
            "make": self.test_make,
            "model": self.test_model
        }

    def test_post_car_success_response(self, mock):
        """Creating a car returns 201"""

        mock_model_exists(mock, model_name=self.test_car_post_body['model'])

        response = self.client.post('/api/cars/', data=self.test_car_post_body)
        self.assertEqual(response.status_code, 201)

    def test_create_car(self, mock):
        """POST creates a car"""
        mock_model_exists(mock, model_name=self.test_car_post_body['model'])

        empty_set = Car.objects.all()
        response = self.client.post('/api/cars/', data=self.test_car_post_body)
        filled_set = Car.objects.all()
        self.assertNotEqual(empty_set, filled_set)

    def test_post_car_response(self, mock):
        """Creating a car returns proper body"""
        mock_model_exists(mock, model_name=self.test_car_post_body['model'])

        response = self.client.post('/api/cars/', data=self.test_car_post_body)
        response_data = response.data['data']
        self.assertEqual(response_data['make'],
                         self.test_car_post_body['make'])
        self.assertEqual(response_data['model'],
                         self.test_car_post_body['model'])

    def test_post_existing_car_error_response(self, mock):
        """Creating an already existing car returns 409"""
        mock_model_exists(mock, model_name=self.test_car_post_body['model'])

        first_post_response = self.client.post(
            '/api/cars/', data=self.test_car_post_body)
        second_post_response = self.client.post(
            '/api/cars/', data=self.test_car_post_body)
        self.assertEqual(first_post_response.status_code, 201)
        self.assertEqual(second_post_response.status_code, 409)

    def test_car_make_too_long_error(self, mock):
        """Creating a car with make over 50 characters returns 400"""
        mock_model_exists(
            mock, model_name=self.test_car_post_body['model'])

        too_long_string = self.__generate_random_string(51)
        post_body = self.test_car_post_body
        post_body['make'] = too_long_string
        response = self.client.post(
            '/api/cars/', data=post_body)
        self.assertEqual(response.status_code, 400)

    def test_car_model_too_long_error(self, mock):
        """Creating a car with model over 50 characters returns 400"""
        too_long_string = self.__generate_random_string(51)

        mock_model_exists(
            mock, model_name=too_long_string)

        post_body = self.test_car_post_body
        post_body['model'] = too_long_string
        response = self.client.post(
            '/api/cars/', data=post_body)
        self.assertEqual(response.status_code, 400)

    def test_car_model_empty_error(self, mock):
        """Creating a car without a model returns 400"""
        mock_model_exists(
            mock, model_name='')

        post_body = {
            'make': self.test_car_post_body['make']
        }
        response = self.client.post(
            '/api/cars/', data=post_body)
        self.assertEqual(response.status_code, 400)

    def test_car_make_empty_error(self, mock):
        """Creating a car without a make returns 400"""
        mock_model_exists(
            mock, model_name=self.test_car_post_body['model'])

        post_body = {
            'model': self.test_car_post_body['model']
        }
        response = self.client.post(
            '/api/cars/', data=post_body)
        self.assertEqual(response.status_code, 400)

    def test_post_throws_error_when_car_doesnt_exist(self, mock):
        """Creating a car that doesn't exist in API returns 400"""
        mock_model_doesnt_exist(mock)

        response = self.client.post(
            '/api/cars/', data=self.test_car_post_body)
        self.assertEqual(response.status_code, 400)
