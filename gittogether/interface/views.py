import pytz
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
from dateutil import parser
from twilio.rest import Client
#from twilio import TwilioRestException
from interface.tokens import getAccountSID, getAuthToken

# Create your views here.

@csrf_exempt
def mainPage(request):
    if request.method == 'POST':
        ID = request.POST['code']
        if request.POST.get("join") and Event.objects.filter(pk = ID):
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
        try:
            schedule_send(phoneNumber, event)
        #except TwilioRestException as e:
        #    return HttpResponse("Schedule time must be between 15 minutes to 7 days.")
        except:
            return HttpResponse("Error has occurred.")
        return HttpResponse("Successfully joined event!")
    if request.method == "GET":
        if(not Event.objects.filter(pk=id)):
            return HttpResponse("An event with that code does not exist")
        curEvent = Event.objects.get(pk=id)
        eventName = curEvent.eventName
        eventDesc = curEvent.eventDesc
        print(curEvent.eventTime)
        print(curEvent.eventTime.astimezone(tz=pytz.UTC))
        return render(request, "joinPage.html", {'eventDesc': eventDesc, 'eventName': eventName})

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
        eastern = timezone("US/Eastern")
        dateEastern = dateBetter.replace(tzinfo=eastern)
        event = Event(eventCode=eventID, eventName=name, eventTime=dateEastern, eventDesc=desc)
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
        body=event.eventName,
        send_at=event.eventTime.astimezone(pytz.UTC),
        schedule_type='fixed',
        to=phoneNumber)
    print(message.sid)
