from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClubViewSet, ClubWorkingHoursViewSet, ZoneViewSet, ZonePriceModifierViewSet, PeripheralViewSet, HardwareProfileViewSet, WorkstationViewSet

router = DefaultRouter()
router.register(r'clubs', ClubViewSet, basename='clubs')
router.register(r'club-working-hourss', ClubWorkingHoursViewSet, basename='club-working-hourss')
router.register(r'zones', ZoneViewSet, basename='zones')
router.register(r'zone-price-modifiers', ZonePriceModifierViewSet, basename='zone-price-modifiers')
router.register(r'peripherals', PeripheralViewSet, basename='peripherals')
router.register(r'hardware-profiles', HardwareProfileViewSet, basename='hardware-profiles')
router.register(r'workstations', WorkstationViewSet, basename='workstations')

urlpatterns = [
    path('', include(router.urls)),
]
