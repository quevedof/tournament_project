from rest_framework import serializers
from .models import Participant, Tournament, TournamentParticipant, Match, MatchParticipant
import random
import string
from datetime import datetime

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
        
        
class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

class TournamentParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentParticipant
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class MatchParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchParticipant
        fields = '__all__'

class CreateTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'number_of_teams')

    def create(self, validated_data):
        # Generate a random 10-character alphanumeric key
        generated_key = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        # Set the current time as the date
        date = datetime.now()

        # Create the Tournament object with the provided data and generated values
        tournament = Tournament.objects.create(
            generated_key=generated_key,
            date=date,
            **validated_data
        )
        return tournament

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
        
        # Create TournamentParticipant associated with the Participant
        tournament_participant = TournamentParticipant.objects.create(
            tournament_id=tournament.id,
            participant=created_participant
        )

        return f"{command_participant_team_name} joined {tournament.name}"
