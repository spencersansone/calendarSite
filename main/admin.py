from django.contrib import admin
from .models import *

class EventList(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ['title']

admin.site.register(Event, EventList)

class EventEntryList(admin.ModelAdmin):
    list_display = ('event',)
    ordering = ['event']

admin.site.register(EventEntry, EventEntryList)
# Register your models here.
