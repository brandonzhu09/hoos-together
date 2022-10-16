import pytz
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from interface.models import Event
import json
from django.views.decorators.csrf import csrf_exempt
from random import randrange
from datetime import datetime, timedelta, timezone, tzinfo
from pytz import timezone
from twilio.rest import Client
from interface.tokens import getAccountSID, getAuthToken

# Create your views here.

@csrf_exempt
def mainPage(request):
    
    if request.method == 'POST':
        print(request.POST)
        ID = request.POST['code']

        if request.POST.get("join") and not id=="" and Event.objects.filter(eventCode = ID):
            return redirect('/join/' + ID)
        elif request.POST.get("create"):
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
            return redirect('/create/')
    return render(request, "home.html")

@csrf_exempt
def joinPage(request, id):
    if request.method == "POST":
        phoneNumber = request.POST["phoneNumber"]
        event = Event.objects.get(eventCode=id)
        confirm(phoneNumber, event)
        try:
            schedule_send(phoneNumber, event)
        except:
            return HttpResponse("That event is going to happen in less than 15 minutes")
        eventName = event.eventName
        eventDesc = event.eventDesc
        eventDate = event.eventTime
        return render(request, "joinPage.html", {'eventDesc': eventDesc, 'eventName': eventName, 'eventDate': eventDate})
    if request.method == "GET":
        if(not Event.objects.filter(pk=id)):
            return HttpResponse("An event with that code does not exist")
        curEvent = Event.objects.get(pk=id)
        eventName = curEvent.eventName
        eventDesc = curEvent.eventDesc
        eventDate = curEvent.eventTime
        print(curEvent.eventTime)
        print(curEvent.eventTime +timedelta(hours=4))
        return render(request, "joinPage.html", {'eventDesc': eventDesc, 'eventName': eventName, 'eventDate': eventDate})

@csrf_exempt
def createPage(request):
    eventID=randrange(100000, 999999)
    print(Event.objects.filter(eventCode=eventID))
    while Event.objects.filter(eventCode=eventID):
        eventID=randrange(100000, 999999)
    if request.method == 'POST':
        name = request.POST.get("name")
        desc = request.POST.get("event")
        date = request.POST.get("date")
        dateBetter = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        event = Event(eventCode=eventID, eventName=name, eventTime=dateBetter, eventDesc=desc)
        event.save()
        return redirect(request.session['login_from'] + 'code/' + str(eventID))
    return render(request, 'createPage.html')

@csrf_exempt
def codePage(request, code):
    return render(request, "codePage.html", {'eventID': code})

def schedule_send(phoneNumber, event):
    account_sid = getAccountSID()
    auth_token = getAuthToken()
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        messaging_service_sid='MGb902be7f3756eed60fe311ab72cc7319',
        body="Reminder: "+event.eventName+  " is about to happen in 15 minutes",
        send_at= event.eventTime +timedelta(hours=4, minutes=-15),
        schedule_type='fixed',
        to="+1" + phoneNumber)
    print(message.sid)

def confirm(phoneNumber, event):
    account_sid = getAccountSID()
    auth_token = getAuthToken()
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        messaging_service_sid='MGb902be7f3756eed60fe311ab72cc7319',
        body="You're confirmed for the " + event.eventName + " at " + event.eventTime.strftime("%I:%M%p on %b %d"),
        to="+1" + phoneNumber)
    print(message.sid)
