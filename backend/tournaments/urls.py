from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TournamentViewSet, TeamViewSet, TeamMemberViewSet, TournamentParticipantViewSet, MatchViewSet

router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet, basename='tournaments')
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'team-members', TeamMemberViewSet, basename='team-members')
router.register(r'tournament-participants', TournamentParticipantViewSet, basename='tournament-participants')
router.register(r'matchs', MatchViewSet, basename='matchs')

urlpatterns = [
    path('', include(router.urls)),
]
