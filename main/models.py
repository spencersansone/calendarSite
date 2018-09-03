from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    repeat_event = models.BooleanField()
    sunday = models.BooleanField()
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    
class EventEntry(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField()
    completed = models.BooleanField()

# Create your models here.
