from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, WorkstationGameViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='games')
router.register(r'workstation-games', WorkstationGameViewSet, basename='workstation-games')

urlpatterns = [
    path('', include(router.urls)),
]
