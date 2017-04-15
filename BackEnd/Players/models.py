from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=100, blank=False, unique=True)
    professional = models.BooleanField(blank=False)


class Player(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class Pitcher(models.Model):
    opponents_free_bases = models.IntegerField(blank=False)
    opponents_singles = models.IntegerField(blank=False)
    opponents_doubles = models.IntegerField(blank=False)
    opponents_triples = models.IntegerField(blank=False)
    opponents_homeruns = models.IntegerField(blank=False)
    opponents_strikeouts = models.IntegerField(blank=False)
    opponents_at_bats = models.IntegerField(blank=False)
    player = models.OneToOneField(Player, on_delete=models.CASCADE, default=None)


class Batter(models.Model):
    free_bases = models.IntegerField(blank=False)
    singles = models.IntegerField(blank=False)
    doubles = models.IntegerField(blank=False)
    triples = models.IntegerField(blank=False)
    homeruns = models.IntegerField(blank=False)
    strikeouts = models.IntegerField(blank=False)
    at_bats = models.IntegerField(blank=False)
    player = models.OneToOneField(Player, on_delete=models.CASCADE, default=None)
