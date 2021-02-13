from django.conf.urls import url
from rest_framework import routers

from .api import CarViewset, RatingViewset, PopularCarViewset

router = routers.SimpleRouter()
router.register(r'cars', CarViewset)
router.register(r'rate', RatingViewset, basename='rate')
router.register(r'popular', PopularCarViewset)

urlpatterns = []

urlpatterns += router.urls
