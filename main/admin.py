from django.contrib import admin
from .models import *

class EventList(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ['title']

admin.site.register(Event, EventList)
# Register your models here.
