from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Game, WorkstationGame
from .serializers import GameSerializer, WorkstationGameSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class WorkstationGameViewSet(viewsets.ModelViewSet):
    queryset = WorkstationGame.objects.all()
    serializer_class = WorkstationGameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

