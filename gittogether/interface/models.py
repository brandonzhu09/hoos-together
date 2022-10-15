from django.db import models

# Create your models here.
class Event(models.Model):
    eventCode = models.IntegerField(primary_key = True)
    eventName = models.TextField(max_length=25, blank=False)
    eventTime = models.DateTimeField(blank=False)
    eventDesc = models.TextField(max_length=100)