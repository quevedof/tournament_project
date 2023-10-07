from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import generics
from .models import Tournament, Match, MatchParticipant, Participant
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

class GetTournamentOverallView(generics.RetrieveAPIView):

    def get_matches(self, tournament_id):
        matches = Match.objects.filter(tournament_id=tournament_id)
        match_participants = MatchParticipant.objects.filter(match__in=matches)
        participants = Participant.objects.filter(id__in=map(lambda mp: mp.participant_id, match_participants))

        participants_dict = dict()
        for p in participants:
            participants_dict[p.id] = p.team_name
        
        # Group MatchParticipant objects by match ID
        match_participants_by_match = {}
        for match_participant in match_participants:
            match_id = match_participant.match_id
            if match_id not in match_participants_by_match:
                match_participants_by_match[match_id] = []
            match_participants_by_match[match_id].append(match_participant)
            
        # Serialize matches with participants
        matches_data = []
        for match in matches:
            match_participants_data = match_participants_by_match.get(match.id, [])
            participants_data = [
                {
                    'id': mp.participant.id,
                    'teamName': participants_dict[mp.participant.id],
                    'score': mp.score,
                }
                for mp in match_participants_data
            ]
            match_data = {
                'id': match.id,
                'date': match.date,
                'participants': participants_data,
                'winner': match.winning_participant_id,
                'nextMatchId': match.next_match_id,
            }
            matches_data.append(match_data)

        return matches_data
    
    def get_tournament(self, tournament_key):
        return Tournament.objects.get(generated_key=tournament_key)

    def retrieve(self, request, *args, **kwargs):
        tournament = self.get_tournament(self.kwargs.get('tournament_key'))
        matches_data = self.get_matches(tournament.id)
        
        response_data = {
            'id': tournament.id,
            'name': tournament.name,
            'generatedKey': tournament.generated_key,
            'matches': matches_data,
        }
        return Response(response_data)

