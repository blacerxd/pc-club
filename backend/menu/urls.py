from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuCategoryViewSet, MenuItemViewSet

router = DefaultRouter()
router.register(r'menu-categorys', MenuCategoryViewSet, basename='menu-categorys')
router.register(r'menu-items', MenuItemViewSet, basename='menu-items')

urlpatterns = [
    path('', include(router.urls)),
]
