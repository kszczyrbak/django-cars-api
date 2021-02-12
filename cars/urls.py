from django.conf.urls import url
from rest_framework import routers

from .api import CarViewset, RatingViewset

router = routers.SimpleRouter()
router.register(r'cars', CarViewset)
router.register(r'rate', RatingViewset, basename='rate')

urlpatterns = []

urlpatterns += router.urls
