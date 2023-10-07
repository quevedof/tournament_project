from rest_framework.response import Response
from rest_framework import viewsets, generics
from .models import Participant, Tournament, TournamentParticipant, Match, MatchParticipant
from .serializers import ParticipantSerializer, CreateTournamentSerializer, TournamentSerializer, TournamentParticipantSerializer, MatchSerializer, MatchParticipantSerializer, JoinTournamentSerializer

class TournamentViewSet(viewsets.ModelViewSet):
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

class CreateTournamentView(generics.CreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = CreateTournamentSerializer
    
class JoinTournamentView(generics.CreateAPIView):
    serializer_class = JoinTournamentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(response_data)
