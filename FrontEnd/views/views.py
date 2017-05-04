from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import requests
import json
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .form import TeamForm, PlayerForm, PitcherForm, BatterForm


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


@ensure_csrf_cookie
def createRoster(request):
    if request.method == 'POST':
        playerForm = PlayerForm(request.POST)
        pitcherForm = PitcherForm(request.POST)
        batterForm = BatterForm(request.POST)
        team_id = request.POST.get('team_select')

        if playerForm.is_valid():
            payload = {'first_name': request.POST.get('first_name'), 'last_name': request.POST.get('last_name')}
            if pitcherForm.is_valid():
                payload['opponents_free_bases'] = request.POST.get('opponents_free_bases')
                payload['opponents_singles'] = request.POST.get('opponents_singles')
                payload['opponents_doubles'] = request.POST.get('opponents_doubles')
                payload['opponents_triples'] = request.POST.get('opponents_triples')
                payload['opponents_homeruns'] = request.POST.get('opponents_homeruns')
                payload['opponents_strikeouts'] = request.POST.get('opponents_strikeouts')
                payload['opponents_at_bats'] = request.POST.get('opponents_at_bats')
            else:
                pitcherForm = PitcherForm()

            if batterForm.is_valid():
                payload['free_bases'] = request.POST.get('free_bases')
                payload['singles'] = request.POST.get('singles')
                payload['doubles'] = request.POST.get('doubles')
                payload['triples'] = request.POST.get('triples')
                payload['homeruns'] = request.POST.get('homeruns')
                payload['strikeouts'] = request.POST.get('strikeouts')
                payload['at_bats'] = request.POST.get('at_bats')
            else:
                batterForm = BatterForm()

            req = requests.post('http://buisness-api:8000/addToRoster/' + str(team_id), data=payload)
            req_json = req.json()
            if req_json['status'] == 'success':
                requests.get('http://localhost:8000/createRoster')
        else:
            playerForm = PlayerForm()
            pitcherForm = PitcherForm()
            batterForm = BatterForm()

    else:
        playerForm = PlayerForm()
        pitcherForm = PitcherForm()
        batterForm = BatterForm()


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
        return render(request, "views/roster.html", {'teams': teams_json['teams'], 'range': range(1, 10),
                                                     'batters': batters_json['team'], 'pitchers': pitchers_json['team'],
                                                     'playerForm': playerForm, 'pitcherForm': pitcherForm,
                                                     'batterForm': batterForm})
    else:
        return render(request, "views/roster.html", {'playerForm': playerForm, 'pitcherForm': pitcherForm,
                                                     'batterForm': batterForm})


def updateTeamSelect(request, pk):
    url = 'http://buisness-api:8000/GetBattersFromTeam/' + str(pk)
    batters = requests.get(url)
    batters_json = batters.json()
    team_data = {}
    if batters_json['status'] == 'error' and batters_json['message'] == 'No batters on this team':
        team_data['batters'] = []
    else:
        team_data['batters'] = batters_json['team']
    pitcher_url = 'http://buisness-api:8000/GetPitchersFromTeam/' + str(pk)
    pitchers = requests.get(pitcher_url)
    pitchers_json = pitchers.json()
    if pitchers_json['status'] == 'error' and pitchers_json['message'] == 'No pitchers on this team':
        team_data['pitchers'] = []
    else:
        team_data['pitchers'] = pitchers_json['team']
    return JsonResponse(team_data)


@ensure_csrf_cookie
def createTeam(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            payload = {'team_name': request.POST.get('team_name'), 'professional': request.POST.get('professional')}
            req = requests.post('http://buisness-api:8000/createTeam', data=payload)
            req_json = req.json()

            return HttpResponseRedirect("/", req_json)
    else:
        form = TeamForm()

    teams = requests.get('http://buisness-api:8000/GetAllTeams')
    teams_json = teams.json()

    return render(request, "views/newTeam.html", {'form': form, 'teams': teams_json['teams']})


def viewTeams(request):
    teams = requests.get('http://buisness-api:8000/GetAllTeams')
    teams_json = teams.json()
    if teams_json['status'] == "success":
        return render(request, "views/viewTeams.html", {'teams': teams_json['teams'], 'errors': ""})
    else:
        return render(request, "views/viewTeams.html", {'teams': teams_json['teams'], 'errors': teams_json['message']})


def viewTeam(request, pk):
    team = requests.get('http://buisness-api:8000/GetTeam/' + pk)
    team_json = team.json()
    errors = ""
    if team_json['status'] == "success":

        batter_url = 'http://buisness-api:8000/GetBattersFromTeam/' + pk
        batters = requests.get(batter_url)
        batters_json = batters.json()
        if batters_json['status'] == "error":
            errors += "No Batter Data for the " + team_json['teams']['team_name'] + "."
            batters_json['team'] = []
        pitcher_url = 'http://buisness-api:8000/GetPitchersFromTeam/' + pk
        pitchers = requests.get(pitcher_url)
        pitchers_json = pitchers.json()

        if pitchers_json['status'] == "error":
            errors += " No pitcher data for the " + team_json['teams']['team_name'] + "."
            pitchers_json['team'] = []

        return render(request, "views/viewTeam.html", {'team': team_json['teams'], 'batters': batters_json['team'],
                                                       'pitchers': pitchers_json['team'], 'errors': errors})

    else:
        errors += "There is no team with team id " + pk + "."

    return render(request, "views/viewTeam.html", {'team': {'team_name': "Not Available"}, 'batters': [],
                                                   'pitchers': [], 'errors': errors})


def viewPlayers(request):
    req = requests.get("http://buisness-api:8000/GetAllPlayers")
    req_json = req.json()
    errors = ""
    if req_json['status'] == "errors":
        errors = req_json['message']
    return render(request, "views/viewPlayers.html", {'players': req_json['players'], 'errors': errors})


def viewPlayer(request, pk):
    req = requests.get("http://buisness-api:8000/GetPlayerData/" + pk)
    req_json = req.json()
    errors = req_json['message']
    if req_json['status'] == "errors":
        errors = req_json['message']
        return render(request, "views/viewPlayer.html", {'players': [], 'errors': errors, 'pitcher': [], 'batter': []})
    else:
        return render(request, "views/viewPlayer.html", {'player': req_json['data']['player'], 'errors': errors,
                                                         'pitcher': req_json['data']['pitcher'],
                                                         'batter': req_json['data']['batter']})
