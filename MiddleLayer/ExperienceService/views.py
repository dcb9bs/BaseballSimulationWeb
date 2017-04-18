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


def GetBattersFromTeam(request, pk):
    req = requests.get('http://models-api:8000/api/v1/batters/' + pk)
    req_json = req.json()
    ret = {'status': 'success'}
    team = []
    for p in req_json['batters']:
        team.append({'id': p['stats']['id'], 'full_name': p['first_name'] + ' ' + p['last_name']})
    ret['team'] = team
    return JsonResponse(ret)


def GetPitchersFromTeam(request, pk):
    req = requests.get('http://models-api:8000/api/v1/pitchers/' + pk)
    req_json = req.json()
    ret = {'status': 'success'}
    team = []
    for p in req_json['pitchers']:
        team.append({'id': p['stats']['id'], 'full_name': p['first_name'] + ' ' + p['last_name']})
    ret['team'] = team
    return JsonResponse(ret)
