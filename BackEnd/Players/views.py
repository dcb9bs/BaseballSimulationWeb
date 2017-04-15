from django.shortcuts import render
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .models import Team, Player
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .serializers import TeamSerializer, PlayerSerializer


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
            return JsonResponse({'status': 'error', 'message': 'No players on this team' })

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
