from django import render
from models import Event

# Create your views here.

def mainPage(request):
    return 3



def joinPage(request):
    if request.method == "POST":
        phoneNumber = request.POST["phoneNumber"]
        eventId = request.path
        curEvent = Event.objects.get(pk=eventId)
    if request.method == "GET":
        eventId = request.path
        eventDesc = 3
        eventName = "Hello"
        return render(request, "templates/joinPage.html", {'eventDesc': eventDesc, 'eventName': eventName})


