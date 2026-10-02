from rest_framework import serializers
from .models import Game, WorkstationGame

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class WorkstationGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkstationGame
        fields = '__all__'

