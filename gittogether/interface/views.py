from django.shortcuts import render
from interface.models import Event
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.

def mainPage(request):
    return 3


@csrf_exempt
def joinPage(request, id):
    if request.method == "POST":
        phoneNumber = request.POST["phoneNumber"]
        return HttpResponse(str(id) + "yeay")
    if request.method == "GET":
        eventId = request.path
        eventDesc = 3
        eventName = "Hello"
        return render(request, "joinPage.html", {'eventDesc': eventDesc, 'eventName': eventName})


