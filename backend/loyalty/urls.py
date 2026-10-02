from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoyaltyAccountViewSet, LoyaltyTransactionViewSet, LoyaltyRuleViewSet

router = DefaultRouter()
router.register(r'loyalty-accounts', LoyaltyAccountViewSet, basename='loyalty-accounts')
router.register(r'loyalty-transactions', LoyaltyTransactionViewSet, basename='loyalty-transactions')
router.register(r'loyalty-rules', LoyaltyRuleViewSet, basename='loyalty-rules')

urlpatterns = [
    path('', include(router.urls)),
]
