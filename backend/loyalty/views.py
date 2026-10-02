from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import LoyaltyAccount, LoyaltyTransaction, LoyaltyRule
from .serializers import LoyaltyAccountSerializer, LoyaltyTransactionSerializer, LoyaltyRuleSerializer

class LoyaltyAccountViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyAccount.objects.all()
    serializer_class = LoyaltyAccountSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LoyaltyTransactionViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyTransaction.objects.all()
    serializer_class = LoyaltyTransactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LoyaltyRuleViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyRule.objects.all()
    serializer_class = LoyaltyRuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

