from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Tournament, Team, TeamMember, TournamentParticipant, Match
from .serializers import TournamentSerializer, TeamSerializer, TeamMemberSerializer, TournamentParticipantSerializer, MatchSerializer

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TournamentParticipantViewSet(viewsets.ModelViewSet):
    queryset = TournamentParticipant.objects.all()
    serializer_class = TournamentParticipantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

