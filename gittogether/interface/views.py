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
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
            return redirect('/create/')
    return render(request, "home.html")

@csrf_exempt
def joinPage(request, id):
    if request.method == "POST":
        phoneNumber = request.POST["phoneNumber"]
        return HttpResponse(str(id) + "yaay")
    if request.method == "GET":
        eventDesc = 3
        eventName = "Hello"
        return render(request, "joinPage.html", {'eventDesc': eventDesc, 'eventName': eventName})

@csrf_exempt
def createPage(request):
    eventID=randrange(100000, 999999)
    if request.method == 'POST':
        name = request.POST.get("name")
        desc = request.POST.get("event")
        date = request.POST.get("date")
        dateBetter = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        eastern = timezone('US/Eastern')
        dateBetter = dateBetter.replace(tzinfo=eastern)
        event = Event(eventCode=eventID, eventName=name, eventTime=dateBetter, eventDesc=desc)
        event.save()
        return redirect(request.session['login_from'] + 'code/' + str(eventID))
    return render(request, 'createPage.html')

@csrf_exempt
def codePage(request, code):
    return render(request, "codePage.html", {'eventID': code})

