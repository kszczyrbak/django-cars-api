from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from cars.models import Car, Rating
from cars.serializers import PopularCarSerializer


class PopularCarListTestCase(APITestCase):

    def __add_test_car(self, **kwargs):
        car = Car.objects.create(**kwargs)
        self.test_cars.append(car)
        return car

    def __add_test_rating(self, car, value):
        rating = Rating.objects.create(car=car, value=value)
        self.test_ratings.append(rating)
        self.car_ratings[car.model] += 1
        return rating

    def setUp(self):
        self.test_cars = []
        self.test_car_1 = self.__add_test_car(make='Honda', model='Civic')
        self.test_car_2 = self.__add_test_car(make='Audi', model='A4')
        self.car_ratings = {car.model: 0 for car in self.test_cars}

        self.test_ratings = []
        self.__add_test_rating(car=self.test_car_1, value='3')
        self.__add_test_rating(car=self.test_car_1, value='4')
        self.__add_test_rating(car=self.test_car_2, value='5')

    def test_success_code(self):
        """Listing popular cars returns 200"""
        response = self.client.get('/api/popular/')
        self.assertEqual(response.status_code, 200)

    def test_success_response(self):
        """Listing popular cars returns proper fields"""
        response = self.client.get('/api/popular/')
        data = response.data['results']
        response_data = PopularCarSerializer(data, many=True).data
        expected_data = PopularCarSerializer(self.test_cars, many=True).data

        for car in expected_data:
            car['num_ratings'] = self.car_ratings[car['model']]

        self.assertEqual(response_data, expected_data)

    def test_empty_response(self):
        """Returns empty list if no cars exist in database"""
        Car.objects.all().delete()
        response = self.client.get(f'/api/popular/')
        data = response.data['results']
        self.assertEqual(data, [])
        self.assertEqual(response.status_code, 200)

    def test_popular_ordering(self):
        """Popular cars are sorted by num_ratings descending"""

        response = self.client.get('/api/popular/')
        data = response.data['results']
        response_data = PopularCarSerializer(data, many=True).data
        num_ratings = [int(car['num_ratings']) for car in response_data]

        is_sorted_descending = all(num_ratings[i] >= num_ratings[i+1]
                                   for i in range(len(num_ratings), -1))

        self.assertTrue(is_sorted_descending)
