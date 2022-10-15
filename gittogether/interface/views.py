from django.shortcuts import render
from django.http import HttpResponse
import json
from models import Event

# Create your views here.



def mainPage(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode("utf-8"))
        eventID = json_data.get('code')
        if Event.objects.filter(eventCode=eventID):
            pass
        else:
            
            
        