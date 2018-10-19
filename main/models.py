from django.db import models
from datetime import datetime

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    location = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
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
    date = models.DateField()
    
    @property
    def current_status(self):
        now = datetime.now()
        
        end_time = self.event.end_time
        start_time = self.event.start_time
        
        
        # -1 --> upcoming
        # 0 --> current
        # 1 --> passed
        
        if now.hour < start_time.hour:
            return -1
        elif now.hour == start_time.hour:
            if now.minute < start_time.minute:
                return -1
            elif now.minute == start_time.minute:
                return 0
            elif now.minute > start_time.minute:
                if now.hour < end_time.hour:
                    return 0
                elif now.hour == end_time.hour:
                    if now.minute <= end_time.minute:
                        return 0
                    else:
                        return 1
        else:
            return 1
            
# Create your models here.
