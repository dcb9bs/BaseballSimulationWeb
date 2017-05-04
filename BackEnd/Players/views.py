from django.shortcuts import render
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .models import Team, Player, Batter, Pitcher
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .serializers import TeamSerializer, PlayerSerializer, BatterSerializer, PitcherSerializer


class TeamList(APIView):
    @csrf_exempt
    def get(self, request):
        # get all teams
        teams = Team.objects.all().values('id', 'team_name', 'professional')
        if len(teams) > 0:
            return JsonResponse({'status': 'success', 'teams': list(teams)})
        else:
            return JsonResponse({'status': 'error', 'message': 'There are no teams'})

    @csrf_exempt
    def post(self, request):
        # create a new team
        team_name = request.POST.get('team_name')
        serialized_team = TeamSerializer(data=request.data)
        if serialized_team.is_valid():
            serialized_team.save()
            try:
                team = Team.objects.get(team_name=team_name)
                return JsonResponse({'status': 'success', 'teams': model_to_dict(team, fields=('id', 'team_name',
                                                                                               'professional'))})
            except Team.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Team was not created successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing required field(s)'})


class TeamDetail(APIView):
    @csrf_exempt
    def get(self, request, pk):
        # get the details of a given team
        try:
            team = Team.objects.get(id=pk)
        except Team.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This team does not exist'})

        return JsonResponse({'status': 'success', 'teams': model_to_dict(team,
                                                                         fields=('id', 'team_name', 'professional'))})

    @csrf_exempt
    def delete(self, request, pk):
        # delete a player given their id
        try:
            team = Team.objects.get(id=pk)
        except Team.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This team does not exist'})
        team_name = team.team_name
        team.delete()
        return JsonResponse({'status': 'success', 'message': team_name + ' deleted successfully'})


class PlayerList(APIView):
    @csrf_exempt
    def get(self, request, pk):
        # get all players on a given team
        try:
            team = Team.objects.get(id=pk)
        except Team.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This team does not exist'})

        try:
            players = Player.objects.all().filter(team_id=team.id).values('id', 'first_name', 'last_name')
        except Player.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No players on this team'})

        if len(players) > 0:
            return JsonResponse({'status': 'success', 'players': list(players)})
        else:
            return JsonResponse({'status': 'error', 'message': 'No players on this team'})

    @csrf_exempt
    def post(self, request, pk):
        # create a player for a given team
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        try:
            Team.objects.get(id=pk)
        except Team.DoesNotExist:
            return JsonResponse({'status': 'error',
                                 'message': 'The team you are trying to create a batter for does not exist.'})

        serialized_player = PlayerSerializer(data=request.data)
        if serialized_player.is_valid():
            serialized_player.save(team_id=pk)
            try:
                player = Player.objects.get(first_name=first_name, last_name=last_name)
                return JsonResponse({'status': 'success',
                                     'players': model_to_dict(player, fields=('id', 'first_name', 'last_name',
                                                                              'team_id'))})
            except Player.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Player was not created successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing required field(s)'})


class PlayerDetail(APIView):
    @csrf_exempt
    def get(self, request, pk):
        # get the details of a given player
        try:
            player = Player.objects.get(id=pk)
        except Player.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This player does not exist'})

        return JsonResponse({'status': 'success', 'players': model_to_dict(player, fields=('id', 'first_name',
                                                                                           'last_name'))})

    @csrf_exempt
    def delete(self, request, pk):
        # delete a player given their id
        try:
            player = Player.objects.get(id=pk)
        except Player.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This player does not exist'})

        player_first_name = player.first_name
        player_last_name = player.last_name
        player.delete()
        return JsonResponse({'status': 'success',
                             'message': player_first_name + ' ' + player_last_name + ' was deleted.'})


class BatterList(APIView):
    @csrf_exempt
    def get(self, request, pk):
        # get all batters on a team
        try:
            Team.objects.get(id=pk)
        except Team.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This team does not exist'})

        try:
            players = Player.objects.all().filter(team_id=pk).values_list('id', 'first_name',
                                                                          'last_name', 'team_id').order_by('id')
        except Player.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No players on this team'})

        return_list = []
        if len(players) > 0:
            for player in players:
                return_dict = {'id': player[0], 'first_name': player[1], 'last_name': player[2], 'team_id': player[3]}
                p = player[0]
                try:
                    batter = Batter.objects.get(player_id=p)
                    return_dict['stats'] = model_to_dict(batter)
                    return_list.append(return_dict)
                except Batter.DoesNotExist:
                    continue

            return JsonResponse({'status': 'success', 'batters': return_list})
        else:
            return JsonResponse({'status': 'error', 'message': 'No batters on this team'})

    @csrf_exempt
    def post(self, request, pk):
        # given a player ID create a batter associated with that player
        try:
            player = Player.objects.get(id=pk)
        except Player.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'The player whose id you entered does not exist'})

        try:
            Batter.objects.get(player_id=pk)
            return JsonResponse({'status': 'error',
                                 'message': 'A batter model has already been created for this player'})
        except Batter.DoesNotExist:
            serialized_batter = BatterSerializer(data=request.data)
            if serialized_batter.is_valid():
                serialized_batter.save(player_id=pk)
                try:
                    batter = Batter.objects.get(player_id=pk)
                except Batter.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Batter was not created successfully.'})

                return JsonResponse({'status': 'success', 'batter': model_to_dict(batter),
                                     'message': player.first_name + ' ' + player.last_name + ' now has batter data'})


class BatterDetail(APIView):
    @csrf_exempt
    def get(self, request, pk):
        # get the stats of a given pitcher
        try:
            batter = Batter.objects.get(id=pk)
        except Batter.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This batter does not exist'})

        return JsonResponse({'status': 'success',
                             'stats': model_to_dict(batter, fields=('id', 'free_bases', 'singles', 'doubles', 'triples',
                                                                    'homeruns', 'strikeouts', 'at_bats', 'player_id'))})

    @csrf_exempt
    def delete(self, request, pk):
        # delete a pitcher given their id
        try:
            batter = Batter.objects.get(id=pk)
        except Batter.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This batter does not exist'})

        try:
            player = Player.objects.get(id=batter.player_id)
        except Player.DoesNotExits:
            return JsonResponse({'status': 'error', 'message': 'There is no player attached to this batter.'})
        player_first_name = player.first_name
        player_last_name = player.last_name
        batter.delete()
        return JsonResponse({'status': 'success',
                             'message': player_first_name + ' ' + player_last_name + "'s batting stats were deleted."})


class PlayerBatterDetail(APIView):
    @csrf_exempt
    def get(self, request, pk):
        # get batter data given a player's id
        try:
            batter = Batter.objects.get(player_id=pk)
        except Batter.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No batter data for this player'})
        return JsonResponse({'status': 'success', 'batter': model_to_dict(batter)})


class PitcherList(APIView):
    @csrf_exempt
    def get(self, request, pk):
        # get all pitchers on a team
        try:
            Team.objects.get(id=pk)
        except Team.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This team does not exist'})

        try:
            players = Player.objects.all().filter(team_id=pk).values_list('id', 'first_name',
                                                                          'last_name', 'team_id').order_by('id')
        except Player.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No players on this team'})

        return_list = []
        if len(players) > 0:
            for player in players:
                return_dict = {'id': player[0], 'first_name': player[1], 'last_name': player[2], 'team_id': player[3]}
                p = player[0]
                try:
                    pitcher = Pitcher.objects.get(player_id=p)
                    return_dict['stats'] = model_to_dict(pitcher)
                    return_list.append(return_dict)
                except Pitcher.DoesNotExist:
                    continue

            return JsonResponse({'status': 'success', 'pitchers': return_list})
        else:
            return JsonResponse({'status': 'error', 'message': 'No pitchers on this team'})

    @csrf_exempt
    def post(self, request, pk):
        # given a player ID create a pitcher associated with that player
        try:
            player = Player.objects.get(id=pk)
        except Player.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'The player whose id you entered does not exist'})

        try:
            Pitcher.objects.get(player_id=pk)
            return JsonResponse({'status': 'error',
                                 'message': 'A pitcher model has already been created for this player'})
        except Pitcher.DoesNotExist:
            serialized_pitcher = PitcherSerializer(data=request.data)
            if serialized_pitcher.is_valid():
                serialized_pitcher.save(player_id=pk)
                try:
                    pitcher = Pitcher.objects.get(player_id=pk)
                except Batter.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Pitcher was not created successfully.'})

                return JsonResponse({'status': 'success', 'pitcher': model_to_dict(pitcher),
                                     'message': player.first_name + ' ' + player.last_name + ' now has pitcher data'})


class PitcherDetail(APIView):
    @csrf_exempt
    def get(self, request, pk):
        # get the stats of a given pitcher
        try:
            pitcher = Pitcher.objects.get(id=pk)
        except Pitcher.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This player does not exist'})

        return JsonResponse({'status': 'success',
                             'stats': model_to_dict(pitcher, fields=('id', 'opponents_free_bases', 'opponents_singles',
                                                                     'opponents_doubles', 'opponents_triples',
                                                                     'opponents_homeruns', 'opponents_strikeouts',
                                                                     'opponents_at_bats', 'player_id'))})

    @csrf_exempt
    def delete(self, request, pk):
        # delete a pitcher given their id
        try:
            pitcher = Pitcher.objects.get(id=pk)
        except Player.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'This pitcher does not exist'})

        try:
            player = Player.objects.get(id=pitcher.player_id)
        except Player.DoesNotExits:
            return JsonResponse({'status': 'error', 'message': 'There is no player attached to this pitcher.'})
        player_first_name = player.first_name
        player_last_name = player.last_name
        pitcher.delete()
        return JsonResponse({'status': 'success',
                             'message': player_first_name + ' ' + player_last_name + "'s pitching stats were deleted."})


class PlayerPitcherDetail(APIView):
    @csrf_exempt
    def get(self, request, pk):
        # get pitcher data given a player's id
        try:
            pitcher = Pitcher.objects.get(player_id=pk)
        except Pitcher.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No pitcher data for this player'})
        return JsonResponse({'status': 'success', 'pitcher': model_to_dict(pitcher)})
