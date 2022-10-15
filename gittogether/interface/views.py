from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from interface.models import Event
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def mainPage(request):
    if request.method == 'POST':
        if request.POST.get("join"):
            ID = request.POST['code']
            if Event.objects.filter(eventCode=ID):
                return render(request, "home.html", message='Code already taken, please enter another code!')
            else:
                return redirect(joinPage)
        elif request.POST.get("create"):
            return redirect('/create/')
    return render(request, "home.html")

def joinPage(request, id):
    if request.method == "POST":
        phoneNumber = request.POST["phoneNumber"]
        return HttpResponse(str(id) + "yaay")
    if request.method == "GET":
        eventId = request.path
        eventDesc = 3
        eventName = "Hello"
        return render(request, "joinPage.html", {'eventDesc': eventDesc, 'eventName': eventName})

def createPage(request):
    return render(request, "createPage.html")

