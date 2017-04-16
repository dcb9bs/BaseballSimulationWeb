from django.shortcuts import render
import requests
from django.http import JsonResponse


def teamSelect(request):
    teams = requests.get('http://buisness-api:8000/GetAllTeams')
    teams_json = teams.json()
    first_team = teams_json['teams'][0]['id']
    url = 'http://buisness-api:8000/GetPlayersFromTeam/' + str(first_team)
    players = requests.get(url)
    players_json = players.json()

    if len(list(teams_json['teams'])) > 0:
        return render(request, "views/index.html", {'teams': teams_json['teams'], 'range': range(1, 10),
                                                    'team': players_json['team']})
    else:
        return render(request, "views/index.html")


def updateTeamSelect(request, pk):
    url = 'http://buisness-api:8000/GetPlayersFromTeam/' + str(pk)
    players = requests.get(url)
    players_json = players.json()
    return JsonResponse({'team': players_json['team']})
