from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from cars.models import Car, Rating
from cars.serializers import RatingPostSerializer


class RatingCreateTestCase(APITestCase):

    def __add_test_car(self, **kwargs):
        car = Car.objects.create(**kwargs)
        self.test_cars.append(car)
        return car

    def __add_test_rating(self, **kwargs):
        test = Rating.objects.create(**kwargs)
        self.test_ratings.append(test)
        return test

    def setUp(self):
        self.test_cars = []
        self.test_ratings = []
        self.test_make = "Honda"
        self.test_model = "Civic"

        self.test_car = self.__add_test_car(
            make=self.test_make, model=self.test_model)

        self.test_post_rating = {
            "car": self.test_car.id,
            "value": 3
        }

    def test_post_rating_success(self):
        """Creating a rating returns 201"""

        response = self.client.post('/api/rate/', data=self.test_post_rating)
        self.assertEqual(response.status_code, 201)

    def test_post_rating_response(self):
        """Creating a rating returns proper body"""

        response = self.client.post('/api/rate/', data=self.test_post_rating)
        self.assertEqual(response.data['data'], self.test_post_rating)

    def test_create_rating(self):
        """POST creates a rating"""

        empty_set = Rating.objects.all()
        response = self.client.post('/api/rate/', data=self.test_post_rating)
        filled_set = Rating.objects.all()
        self.assertNotEqual(empty_set, filled_set)


    def test_rating_of_not_existing_car(self):
        """Creating a rating of unexistent car returns 400"""

        post_body = {
            "car": 99,
            "value": 3
        }
        response = self.client.post(
            '/api/rate/', data=post_body)
        self.assertEqual(response.status_code, 400)

    def test_post_rating_over_range(self):
        """Creating a rating value over 5 returns 400"""

        post_body = self.test_post_rating
        post_body['value'] = 6

        response = self.client.post('/api/rate/', data=post_body)
        self.assertEqual(response.status_code, 400)

    def test_post_rating_under_range(self):
        """Creating a rating value under 1 returns 400"""
        post_body = self.test_post_rating
        post_body['value'] = 0

        response = self.client.post('/api/rate/', data=post_body)
        self.assertEqual(response.status_code, 400)
