from rest_framework import viewsets, generics
from .models import Participant, Tournament, TournamentParticipant, Match, MatchParticipant
from .serializers import ParticipantSerializer, TournamentSerializer, TournamentParticipantSerializer, MatchSerializer, MatchParticipantSerializer

class CreateTournamentView(generics.CreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class TournamentParticipantViewSet(viewsets.ModelViewSet):
    queryset = TournamentParticipant.objects.all()
    serializer_class = TournamentParticipantSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class MatchParticipantViewSet(viewsets.ModelViewSet):
    queryset = MatchParticipant.objects.all()
    serializer_class = MatchParticipantSerializer
