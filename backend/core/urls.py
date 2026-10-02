from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CityViewSet

router = DefaultRouter()
router.register(r'citys', CityViewSet, basename='citys')

urlpatterns = [
    path('', include(router.urls)),
]
