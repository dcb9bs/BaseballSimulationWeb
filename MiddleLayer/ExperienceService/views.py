from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
    if req_json['status'] == 'success':
        ret = {'status': 'success'}
        team = []
        for p in req_json['batters']:
            team.append({'id': p['stats']['id'], 'full_name': p['first_name'] + ' ' + p['last_name']})
        ret['team'] = team
        return JsonResponse(ret)
    else:
        return JsonResponse(req_json)


def GetPitchersFromTeam(request, pk):
    req = requests.get('http://models-api:8000/api/v1/pitchers/' + pk)
    req_json = req.json()
    if req_json['status'] == 'success':
        ret = {'status': 'success'}
        team = []
        for p in req_json['pitchers']:
            team.append({'id': p['stats']['id'], 'full_name': p['first_name'] + ' ' + p['last_name']})
        ret['team'] = team
        return JsonResponse(ret)
    else:
        return JsonResponse(req_json)


@csrf_exempt
def createTeam(request):
    form_data = {'team_name': request.POST.get('team_name')}
    try:
        request['professional']
        form_data['professional'] = True
    except:
        form_data['professional'] = False
    req = requests.post("http://models-api:8000/api/v1/teams", form_data)

    req_json = req.json()

    return JsonResponse(req_json)


