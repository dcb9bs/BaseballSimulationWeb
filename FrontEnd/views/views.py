from django.shortcuts import render
import requests


def teamSelect(request):
    teams = requests.get('http://buisness-api:8000/GetAllTeams')
    teams_json = teams.json()

    # players = request.get('http://buisness-api')

    if len(list(teams_json['teams'])) > 0:
        return render(request, "views/index.html", {'teams': teams_json['teams']})
    else:
        return render(request, "views/index.html")
