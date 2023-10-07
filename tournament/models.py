from django.db import models

# Create your models here.

class Participant(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    team_name = models.CharField(max_length=255, unique=True)

class Tournament(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    generated_key = models.CharField(max_length=255, unique=True)
    number_of_teams = models.IntegerField()
    date = models.DateTimeField()

class TournamentParticipant(models.Model):
    id = models.BigAutoField(primary_key=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.RESTRICT)
    participant = models.ForeignKey(Participant, on_delete=models.RESTRICT)
    
    class Meta:
        unique_together = ('tournament', 'participant')

class Match(models.Model):
    id = models.BigAutoField(primary_key=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.RESTRICT)
    date = models.DateTimeField()
    winning_participant = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, blank=True)
    next_match = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

class MatchParticipant(models.Model):
    id = models.BigAutoField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=models.RESTRICT)
    participant = models.ForeignKey(Participant, on_delete=models.RESTRICT)
    score = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ('match', 'participant')
