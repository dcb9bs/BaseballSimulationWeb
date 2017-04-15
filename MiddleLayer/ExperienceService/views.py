from django.shortcuts import render
import requests
from django.http import JsonResponse


def GetAllTeams(request):
    req = requests.get('http://models-api:8000/api/v1/teams')
    return JsonResponse(req.json())
