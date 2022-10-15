from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def mainPage(request):




def joinPage(request):
    if request.method == "POST":
        phoneNumber = request.POST["phoneNumber"]
        eventId = request.path
    if request.method == "GET":
        eventId = request.path

