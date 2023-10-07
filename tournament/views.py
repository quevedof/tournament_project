from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import generics
from .models import Tournament
from .serializers import CreateTournamentSerializer, JoinTournamentSerializer, TournamentSerializer

class CreateTournamentView(generics.CreateAPIView):
    serializer_class = CreateTournamentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(response_data)
    
class JoinTournamentView(generics.CreateAPIView):
    serializer_class = JoinTournamentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(response_data)

class TournamentByGeneratedKeyView(generics.RetrieveAPIView):
    serializer_class = TournamentSerializer

    def get_object(self):
        generated_key = self.kwargs.get('generated_key')
        try:
            return Tournament.objects.get(generated_key=generated_key)
        except Tournament.DoesNotExist:
            raise NotFound("Tournament not found.")