from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'participants', views.ParticipantViewSet)
router.register(r'tournament-participants', views.TournamentParticipantViewSet)
router.register(r'tournament', views.TournamentViewSet)
router.register(r'matches', views.MatchViewSet)
router.register(r'match-participants', views.MatchParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-tournament', views.CreateTournamentView.as_view(), name='create-tournament'),
    path('join', views.JoinTournamentView.as_view(), name='join'),
    path('tournaments/<str:generated_key>', views.TournamentByGeneratedKeyView.as_view(), name='tournament-by-generated-key'),
]
