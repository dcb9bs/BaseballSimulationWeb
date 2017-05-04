from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


def GetAllTeams(request):
    req = requests.get('http://models-api:8000/api/v1/teams')
    return JsonResponse(req.json())


def GetTeam(request, pk):
    req = requests.get('http://models-api:8000/api/v1/team/' + pk)
    return JsonResponse(req.json())


def GetAllPlayers(request):
    teams = requests.get('http://models-api:8000/api/v1/teams')
    teams_json = teams.json()
    p = []
    if teams_json['status'] == "success":
        for team in teams_json['teams']:
            players = requests.get("http://models-api:8000/api/v1/players/" + str(team['id']))
            players_json = players.json()
            if players_json['status'] == "success":
                for player in list(players_json['players']):
                    p.append({'id': player['id'], 'full_name': player['first_name'] + " " + player['last_name'],
                              'team_id': team['id']})
            else:
                continue
        return_val = {'status': "success", 'players': p}

    else:
        return_val = {'status': "error", 'message': teams_json['message']}

    return JsonResponse(return_val)


def GetPlayersFromTeam(request, pk):
    req = requests.get('http://models-api:8000/api/v1/players/' + pk)
    req_json = req.json()
    ret = {'status': 'success'}
    team = []
    for p in req_json['players']:
        team.append({'id': p['id'], 'full_name': p['first_name'] + ' ' + p['last_name']})
    ret['team'] = team
    return JsonResponse(ret)


def GetPlayerData(request, pk):
    player = requests.get('http://models-api:8000/api/v1/player/' + pk)
    player_json = player.json()
    if player_json['status'] == "success":
        batter = requests.get('http://models-api:8000/api/v1/player/batter/' + pk)
        batter_json = batter.json()
        error = ""
        player_data = {'full_name': player_json['players']['first_name'] + ' ' + player_json['players']['last_name']}
        return_val = {}
        if batter_json['status'] == "error":
            error += batter_json['message']
            return_val['batter'] = []
            return_val['player'] = player_data
        else:
            batting_avg = (batter_json['batter']['singles'] + batter_json['batter']['doubles'] +
                           batter_json['batter']['triples'] + batter_json['batter']['homeruns']) / \
                          batter_json['batter']['at_bats']
            slugging = (batter_json['batter']['singles'] + (batter_json['batter']['doubles'] * 2) +
                        (batter_json['batter']['triples'] * 3) +(batter_json['batter']['homeruns'] * 4)) / \
                       batter_json['batter']['at_bats']
            on_base = (batter_json['batter']['free_bases'] + batter_json['batter']['singles'] +
                       batter_json['batter']['doubles'] + batter_json['batter']['triples'] +
                       batter_json['batter']['homeruns']) / batter_json['batter']['at_bats']
            # runs_created =
            player_data['slugging'] = slugging
            player_data['on_base'] = on_base
            player_data['batting_avg'] = batting_avg
            return_val['player'] = player_data
            return_val['batter'] = batter_json['batter']

        pitcher = requests.get('http://models-api:8000/api/v1/player/pitcher/' + pk)
        pitcher_json = pitcher.json()
        if pitcher_json['status'] == "error":
            error += pitcher_json['message']
            return_val['pitcher'] = []
        else:
            # opp_batting_avg = (pitcher_json['singles'] + pitcher_json['doubles'] + pitcher_json['triples'] +
            #                pitcher_json['homeruns']) / pitcher_json['at_bats']
            # slugging = (batter_json['singles'] + (batter_json['doubles'] * 2) + (batter_json['triples'] * 3) +
            #             (batter_json['homeruns'] * 4)) / batter_json['at_bats']
            # on_base = (batter_json['free_bases'] + batter_json['singles'] + batter_json['doubles'] +
            #           batter_json['triples'] + batter_json['homeruns']) / batter_json['at_bats']
            # runs_created =
            # pitcher_data = {'full_name': batter_json['first_name'] + ' ' + batter_json['last_name'],
            #                'slugging': slugging, 'on_base': on_base, 'batting_avg': opp_batting_avg}
            return_val['pitcher'] = pitcher_json['pitcher']
        return JsonResponse({'status': "success", 'message': error, 'data': return_val})

    else:
        return JsonResponse({'status': "error", 'message': player_json['message']})


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


@csrf_exempt
def addToRoster(request, pk):
    player_req = requests.post("http://models-api:8000/api/v1/players/" + pk,
                               {"first_name": request.POST.get('first_name'),
                                "last_name": request.POST.get('last_name')})
    player_req_json = player_req.json()
    message = ""
    status = ""
    return_val = {}
    if player_req_json['status'] == "success":
        return_val['player'] = player_req_json['players']

        pitcher = request.POST.get('opponents_free_bases')
        if pitcher is not None:
            pitcher_req = requests.post("http://models-api:8000/api/v1/pitchers/" +
                                        str(player_req_json["players"]["id"]),
                                        {'opponents_free_bases': request.POST.get('opponents_free_bases'),
                                         'opponents_singles': request.POST.get('opponents_singles'),
                                         'opponents_doubles': request.POST.get('opponents_doubles'),
                                         'opponents_triples': request.POST.get('opponents_triples'),
                                         'opponents_homeruns': request.POST.get('opponents_homeruns'),
                                         'opponents_strikeouts': request.POST.get('opponents_strikeouts'),
                                         'opponents_at_bats': request.POST.get('opponents_at_bats')})
            pitcher_req_json = pitcher_req.json()
            message += pitcher_req_json['message']
            if pitcher_req_json['status'] == "error":
                status = "error"
            else:
                return_val['pitcher'] = pitcher_req_json['pitcher']

        batter = request.POST.get('free_bases')
        if batter is not None:
            batter_req = requests.post("http://models-api:8000/api/v1/batters/" + str(player_req_json["players"]["id"]),
                                       {'free_bases': request.POST.get('free_bases'),
                                        'singles': request.POST.get('singles'), 'doubles': request.POST.get('doubles'),
                                        'triples': request.POST.get('triples'),
                                        'homeruns': request.POST.get('homeruns'),
                                        'strikeouts': request.POST.get('strikeouts'),
                                        'at_bats': request.POST.get('at_bats')})
            batter_req_json = batter_req.json()
            message += batter_req_json['message']
            if batter_req_json['status'] == "error":
                status = "error"
            else:
                return_val['batter'] = batter_req_json['batter']
    else:
        message += player_req_json['message']
        status = player_req_json['status']

    return_val['status'] = status
    return_val['message'] = message

    return JsonResponse(return_val)
