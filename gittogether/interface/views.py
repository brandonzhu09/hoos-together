from django.shortcuts import render, redirect
from interface.models import Event
import json

# Create your views here.

def mainPage(request):
    if request.method == 'POST':
        if request.POST.get("join"):
            body = json.loads(request.body.decode('utf-8'))
            if Event.objects.filter(eventCode=body['code']):
                pass
            else:
                redirect(joinPage)
        elif request.POST.get("create"):
            redirect(createPage)
    return render(request, "home.html")

def joinPage(request):
    if request.method == "POST":
        phoneNumber = request.POST["phoneNumber"]
        eventId = request.path
        curEvent = Event.objects.get(pk=eventId)
    if request.method == "GET":
        eventId = request.path
        eventDesc = 3
        eventName = "Hello"
        return render(request, "joinPage.html", {'eventDesc': eventDesc, 'eventName': eventName})

def createPage(request):
    return render(request, "createPage.html")

