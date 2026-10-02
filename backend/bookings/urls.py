from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, BookingStatusLogViewSet, WaitlistViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'booking-status-logs', BookingStatusLogViewSet, basename='booking-status-logs')
router.register(r'waitlists', WaitlistViewSet, basename='waitlists')

urlpatterns = [
    path('', include(router.urls)),
]
