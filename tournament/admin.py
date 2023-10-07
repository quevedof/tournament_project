from django.contrib import admin
from .models import Participant, Tournament, TournamentParticipant, Match, MatchParticipant

# Register your models here.

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'team_name')
    search_fields = ('email', 'team_name')

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'generated_key', 'number_of_teams', 'date')
    search_fields = ('name', 'generated_key')

@admin.register(TournamentParticipant)
class TournamentParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournament', 'participant')
    list_filter = ('tournament',)
    search_fields = ('participant__email', 'participant__team_name')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournament', 'date', 'winning_participant', 'next_match')
    list_filter = ('tournament',)
    search_fields = ('tournament__name', 'date')

@admin.register(MatchParticipant)
class MatchParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'participant', 'score')
    list_filter = ('match',)
    search_fields = ('participant__email', 'participant__team_name')
