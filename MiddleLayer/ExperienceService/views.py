from django.shortcuts import render
import requests
from django.http import JsonResponse


def GetAllTeams(request):
    req = requests.get('http://models-api:8000/api/v1/teams')
    return JsonResponse(req.json())


def GetPlayersFromTeam(request, pk):
    req = requests.get('http://models-api:8000/api/v1/players/' + pk)
    req_json = req.json()
    ret = {'status': 'success'}
    team = []
    for p in req_json['players']:
        team.append({'id': p['id'], 'full_name': p['first_name'] + ' ' + p['last_name']})
    ret['team'] = team
    return JsonResponse(ret)
