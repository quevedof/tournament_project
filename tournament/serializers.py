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
