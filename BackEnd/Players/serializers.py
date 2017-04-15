from .models import Team, Player, Pitcher, Batter
from rest_framework import serializers


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'team_name', 'professional')


class PlayerSerializer(serializers.ModelSerializer):
    team_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'first_name', 'last_name', 'team_id')


class PitcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitcher
        fields = ('id', 'opponents_free_bases', 'opponents_singles', 'opponents_doubles', 'opponents_triples',
                  'opponents_homeruns', 'opponents_strikeouts', 'opponents_at_bats')


class BatterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batter
        fields = ('id', 'free_bases', 'singles', 'doubles', 'triples', 'homeruns', 'strikeouts', 'at_bats')
