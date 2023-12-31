# Generated by Django 3.2.22 on 2023-10-07 16:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('next_match', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.match')),
            ],
        ),
        migrations.CreateModel(
            name='MatchParticipant',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.match')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('team_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentParticipant',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.participant')),
            ],
        ),
        migrations.DeleteModel(
            name='Feature',
        ),
        migrations.RenameField(
            model_name='tournament',
            old_name='num_of_teams',
            new_name='number_of_teams',
        ),
        migrations.AddField(
            model_name='tournament',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='generated_key',
            field=models.CharField(default=123, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AddField(
            model_name='tournamentparticipant',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament'),
        ),
        migrations.AddField(
            model_name='matchparticipant',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.participant'),
        ),
        migrations.AddField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament'),
        ),
        migrations.AddField(
            model_name='match',
            name='winning_participant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.participant'),
        ),
        migrations.AlterUniqueTogether(
            name='tournamentparticipant',
            unique_together={('tournament', 'participant')},
        ),
        migrations.AlterUniqueTogether(
            name='matchparticipant',
            unique_together={('match', 'participant')},
        ),
    ]
