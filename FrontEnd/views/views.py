from django.shortcuts import render
import requests
from django.http import JsonResponse


def teamSelect(request):
    teams = requests.get('http://buisness-api:8000/GetAllTeams')
    teams_json = teams.json()
    first_team = teams_json['teams'][0]['id']
    batter_url = 'http://buisness-api:8000/GetBattersFromTeam/' + str(first_team)
    batters = requests.get(batter_url)
    batters_json = batters.json()
    pitcher_url = 'http://buisness-api:8000/GetPitchersFromTeam/' + str(first_team)
    pitchers = requests.get(pitcher_url)
    pitchers_json = pitchers.json()

    if len(list(teams_json['teams'])) > 0:
        return render(request, "views/index.html", {'teams': teams_json['teams'], 'range': range(1, 10),
                                                    'batters': batters_json['team'], 'pitchers': pitchers_json['team']})
    else:
        return render(request, "views/index.html")


def updateTeamSelect(request, pk):
    url = 'http://buisness-api:8000/GetBattersFromTeam/' + str(pk)
    batters = requests.get(url)
    batters_json = batters.json()
    pitcher_url = 'http://buisness-api:8000/GetPitchersFromTeam/' + str(pk)
    pitchers = requests.get(pitcher_url)
    pitchers_json = pitchers.json()
    return JsonResponse({'batters': batters_json['team'], 'pitchers': pitchers_json['team']})
