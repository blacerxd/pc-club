from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, StaffProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'staff-profiles', StaffProfileViewSet, basename='staff-profiles')

urlpatterns = [
    path('', include(router.urls)),
]
