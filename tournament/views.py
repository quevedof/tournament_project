from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import generics, status
from datetime import datetime
from django.db import transaction 
from django.forms.models import model_to_dict
from .models import Tournament, Match, MatchParticipant, Participant, TournamentParticipant, TournamentParticipant
from .serializers import CreateTournamentSerializer, JoinTournamentSerializer, TournamentSerializer, TournamentParticipantsSerializer
import random
from rest_framework.views import APIView


class CreateTournamentView(generics.CreateAPIView):
    serializer_class = CreateTournamentSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(response_data)

class JoinTournamentView(generics.CreateAPIView):
    serializer_class = JoinTournamentSerializer

    @transaction.atomic
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

    def get_matches_response(self, tournament_key):
        tournament = self.get_tournament(tournament_key);
        matches_data = self.get_matches(tournament.id)
        response_data = {
            'id': tournament.id,
            'name': tournament.name,
            'generatedKey': tournament.generated_key,
            'matches': matches_data,
        }
        return Response(response_data)
    
    def retrieve(self, request, *args, **kwargs):
        return self.get_matches_response(self.kwargs.get("tournament_key"))

def randomize_list(input_list):
    # Create a copy of the input list to avoid modifying the original list
    shuffled_list = input_list.copy()
    
    # Shuffle the elements in the copied list
    random.shuffle(shuffled_list)
    
    return shuffled_list

class GenerateMatchesInTournamantView(generics.CreateAPIView):

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        tournament_key = self.kwargs.get('tournament_key')
        tournament = Tournament.objects.get(generated_key=tournament_key)
        
        # Validate request
        tournament_participants = TournamentParticipant.objects.filter(tournament_id=tournament.id)
        if (len(tournament_participants) != tournament.number_of_teams):
            raise ParseError("Not enough participants to start the tournament")
        
        
        if Match.objects.filter(tournament=tournament).count() > 0:
            raise ParseError("Matches already created")

        # Randomises Order
        shuffled_tournament_participants = randomize_list(list(tournament_participants))
            
        number_of_matches_needed = tournament.number_of_teams - 1
        final_match = Match.objects.create(
            tournament=tournament,
            date=datetime.now()
        )
        matches_queue = [final_match]
        number_of_matches_created = 1
        while number_of_matches_created < number_of_matches_needed:
            match = matches_queue.pop(0)
            match_a = Match.objects.create(
                tournament=tournament,
                date=datetime.now(),
                next_match_id=match.id
            )
            match_b = Match.objects.create(
                tournament=tournament,
                date=datetime.now(),
                next_match_id=match.id
            )
            number_of_matches_created += 2
            
            final_round = number_of_matches_created >= (number_of_matches_needed / 2)
            if final_round:
                MatchParticipant.objects.create(
                    match=match_a,
                    participant_id=shuffled_tournament_participants.pop(0).id
                )
                MatchParticipant.objects.create(
                    match=match_a,
                    participant_id=shuffled_tournament_participants.pop(0).id
                )
                MatchParticipant.objects.create(
                    match=match_b,
                    participant_id=shuffled_tournament_participants.pop(0).id
                )
                MatchParticipant.objects.create(
                    match=match_b,
                    participant_id=shuffled_tournament_participants.pop(0).id
                )
            else:
                matches_queue.append(match_a)
                matches_queue.append(match_b)
        
        return Response("Generated")

class TournamentParticipantsAPIView(generics.ListAPIView):
    serializer_class = TournamentParticipantsSerializer

    def get_queryset(self):
        # Retrieve the tournament based on the provided generated_key
        generated_key = self.kwargs['generated_key']
        return TournamentParticipant.objects.filter(tournament__generated_key=generated_key)
    
    
class TournamentParticipantDeleteView(APIView):
    def delete(self, request, tournament_key, participant_id):
        try:
            tournament = Tournament.objects.get(generated_key=tournament_key)
            participant = Participant.objects.get(pk=participant_id)
        except (Tournament.DoesNotExist, Participant.DoesNotExist):
            return Response(
                {"message": "Tournament or participant not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            tournament_participant = TournamentParticipant.objects.get(
                tournament=tournament,
                participant=participant
            )

            tournament_participant.delete()

            participant = Participant.objects.get(pk=participant_id)
            participant.delete()
            
            return Response(
                {"message": "TournamentParticipant deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        except TournamentParticipant.DoesNotExist:
            return Response(
                {"message": "TournamentParticipant not found."},
                status=status.HTTP_404_NOT_FOUND
            )
