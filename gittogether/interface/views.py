from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from interface.models import Event
import json
from django.views.decorators.csrf import csrf_exempt
from random import randrange
from datetime import datetime, timedelta, timezone
from datetime import tzinfo
from pytz import timezone

# Create your views here.

@csrf_exempt
def mainPage(request):
    if request.method == 'POST':
        ID = request.POST['code']
        if request.POST.get("join"):
            if Event.objects.filter(eventCode=ID):
                return render(request, "home.html", message='Code already taken, please enter another code!')
            else:
                return redirect('/join/' + ID)
        elif request.POST.get("create"):
            return redirect('/create/')
    return render(request, "home.html")

@csrf_exempt
def joinPage(request, id):
    if request.method == "POST":
        phoneNumber = request.POST["phoneNumber"]
        return HttpResponse(str(id) + "yaay")
    if request.method == "GET":
        eventId = request.path
        eventDesc = 3
        eventName = "Hello"
        return render(request, "joinPage.html", {'eventDesc': eventDesc, 'eventName': eventName})

@csrf_exempt
def createPage(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        desc = request.POST.get("event")
        date = request.POST.get("date")
        dateBetter = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        eastern = timezone('US/Eastern')
        dateBetter = dateBetter.replace(tzinfo=eastern)
        event = Event(eventCode=randrange(1000000, 9999999), eventName=name, eventTime=dateBetter, eventDesc=desc)
       # 2022-10-21T17:49
        print(event.eventTime)
        event.save()
    return render(request, "createPage.html")

