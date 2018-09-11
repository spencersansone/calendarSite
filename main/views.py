from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from datetime import datetime, date, timedelta

def getTodayDateTime():
    return datetime.now()

def getTodayDate():
    return date.today()
    
def getWeekdayArray():
    return ["monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday"]

def home(request):
    return render(request, 'main/home.html')
    
def event_list(request):
    all_events = Event.objects.all()
    print(all_events)
    x = {}
    x['event_list'] = all_events
    return render(request, 'main/event_list.html', x)
    
def add_event(request):
    def sanitize_time(var):
        if 'am' in var or 'pm' in var:
            split = var.split(':')
            split_1 = split[1]
            
            hour = split[0]
            minute = split_1[:2]
            meridiem = split_1[2:4]
            
            if meridiem == "am":
                if hour == "12":
                    hour = "00"
                elif int(hour) < 10:
                    hour = "0" + hour
            elif meridiem == "pm":
                if hour != "12":
                    hour = "{}".format(int(hour) + 12)
            return "{}:{}".format(hour,minute)
        return var
    
    
    
    if request.method == "POST":
        t = request.POST.get('title')
        print(t)
        d = request.POST.get('description')
        print(d)
        l = request.POST.get('location')
        print(l)
        s_d = request.POST.get('start_date')
        print(s_d)
        s_t = request.POST.get('start_time')
        print(s_t)
        print("{} CLEAN start".format(sanitize_time(s_t)))
        e_d = request.POST.get('end_date')
        print(e_d)
        e_t = request.POST.get('end_time')
        print(e_t)
        print("{} CLEAN end".format(sanitize_time(e_t)))
        no_repeat = True if request.POST.get('no_repeat') == "on" else False
        print("no rep?")
        print(no_repeat)
        yes_repeat = True if request.POST.get('yes_repeat') == "on" else False
        print("yes rep?")
        print(yes_repeat)
        
        r_e = False
        sun = False
        mon = False
        tue = False
        wed = False
        thu = False
        fri = False
        sat = False
        if yes_repeat:
            r_e = True
            sun = True if request.POST.get('sunday') == "on" else False
            mon = True if request.POST.get('monday') == "on" else False
            tue = True if request.POST.get('tuesday') == "on" else False
            wed = True if request.POST.get('wednesday') == "on" else False
            thu = True if request.POST.get('thursday') == "on" else False
            fri = True if request.POST.get('friday') == "on" else False
            sat = True if request.POST.get('saturday') == "on" else False

        
        
        
        Event.objects.create(
            title = t,
            description = d,
            location = l,
            start_date = s_d,
            start_time = sanitize_time(s_t),
            end_date = e_d,
            end_time = sanitize_time(e_t),
            repeat_event = r_e,
            sunday = sun,
            monday = mon,
            tuesday = tue,
            wednesday = wed,
            thursday = thu,
            friday = fri,
            saturday = sat)
        
        # return render(request, 'main/event_list.html')
        return HttpResponseRedirect(reverse('main:event_list'))
        
    return render(request, 'main/add_event.html')
    
def today_agenda(request):
    


    today = getTodayDateTime()
    today_weekday = getWeekdayArray()[today.weekday()]
    query1 = Q(**{today_weekday: True})
    query2 = Q(start_date=today)
    today_events = Event.objects.filter( query1 | query2 )
    
    for event in today_events:
        today_event_entries = EventEntry.objects.filter(
            event = event,
            datetime_created__year = today.year,
            datetime_created__month = today.month,
            datetime_created__day = today.day)
        
        if len(today_event_entries) == 0:
            event_entry = EventEntry.objects.create(
                event = event,
                datetime_created = today,
                completed = False,
                start_date = today)
                
    routine_events = Event.objects.filter(repeat_event=True)
    

    
    t = getTodayDate()
    x = t - timedelta(days=365)
    dates = []
    while x <= t:
        dates += [x]
        x += timedelta(days=1)
        
    all_event_entries = EventEntry.objects.all()
    for event in routine_events:
        weekday_list = []
        
        if event.monday:
            weekday_list += [0]
        if event.tuesday:
            weekday_list += [1]
        if event.wednesday:
            weekday_list += [2]
        if event.thursday:
            weekday_list += [3]
        if event.friday:
            weekday_list += [4]
        if event.saturday:
            weekday_list += [5]
        if event.sunday:
            weekday_list += [6]
        relevant_dates = []
        for date in dates:
            if date.weekday() in weekday_list:
                same_entries = all_event_entries.filter(
                    event = event,
                    start_date = date)
                if len(same_entries) == 0:
                    EventEntry.objects.create(
                        event = event,
                        datetime_created = today,
                        completed = False,
                        start_date = date)
        print(relevant_dates)
            
        



    x = {}
    # x['event_entries'] = EventEntry.objects.filter(
    #     datetime_created__year = today.year,
    #     datetime_created__month = today.month,
    #     datetime_created__day = today.day).order_by('event__start_time')
    x['event_entries'] = EventEntry.objects.filter(
        start_date = today).order_by('event__start_time')
    
    return render(request, 'main/today_agenda.html', x)

# Create your views here.
