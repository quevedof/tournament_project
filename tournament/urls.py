from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('create-tournament', views.CreateTournamentView.as_view(), name='create-tournament'),
    path('join', views.JoinTournamentView.as_view(), name='join'),
    path('tournaments/<str:generated_key>', views.TournamentByGeneratedKeyView.as_view(), name='tournament-by-generated-key'),
    path('tournaments/<str:tournament_key>/overall', views.GetTournamentOverallView.as_view(), name='generate-matches'),
]
