from rest_framework import serializers
from .models import Participant, Tournament, TournamentParticipant, Match, MatchParticipant
import random
import string
from datetime import datetime

class CreateTournamentSerializer(serializers.Serializer):
    name = serializers.CharField()
    numberOfTeams = serializers.DecimalField(max_digits=2, decimal_places=0)

    def create(self, validated_data):
        command_name = validated_data.pop('name')
        command_number_of_teams = validated_data.pop('numberOfTeams')
        
        # Generate a random 10-character alphanumeric key
        generated_key = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        # Create the Tournament object with the provided data and generated values
        tournament = Tournament.objects.create(
            generated_key=generated_key,
            date=datetime.now(),
            name=command_name,
            number_of_teams=command_number_of_teams
        )

        return {
            "name": tournament.name,
            "numberOfTeams": tournament.number_of_teams,
            "generatedKey": tournament.generated_key,
            "date": tournament.date,
        }

class JoinTournamentSerializer(serializers.Serializer):
    teamName = serializers.CharField()
    email = serializers.CharField()
    tournamentKey = serializers.CharField()

    def create(self, validated_data):
        
        command_participant_team_name = validated_data.pop('teamName')
        command_participant_email = validated_data.pop('email')
        command_tournament_key = validated_data.pop('tournamentKey')
        
        # Create Participant
        created_participant = Participant.objects.create(
            email=command_participant_email,
            team_name=command_participant_team_name,
        )

        tournament = Tournament.objects.filter(generated_key=command_tournament_key).first()
        number_of_current_participants = TournamentParticipant.objects.filter(tournament=tournament.id).count()
        if tournament.number_of_teams <= number_of_current_participants:
            raise Exception("Tournament is already full")
        
        # Create TournamentParticipant associated with the Participant
        tournament_participant = TournamentParticipant.objects.create(
            tournament_id=tournament.id,
            participant=created_participant
        )

        return f"{command_participant_team_name} joined {tournament.name}"

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        camel_case_data = {}
        for key, value in data.items():
            camel_case_key = ''.join(word.capitalize() if index > 0 else word for index, word in enumerate(key.split('_')))
            camel_case_data[camel_case_key] = value
        return camel_case_data
    
class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'email', 'team_name')

class TournamentParticipantsSerializer(serializers.ModelSerializer):
    participant_id = serializers.IntegerField(source='participant.id')
    email = serializers.EmailField(source='participant.email')
    team_name = serializers.CharField(source='participant.team_name')

    class Meta:
        model = TournamentParticipant
        fields = ('participant_id', 'email', 'team_name')  # Include other 