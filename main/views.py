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
    # standard time variable function
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
    
    
    # post data action
    if request.method == "POST":
        add_another = request.POST.get('add_another')
        t = request.POST.get('title')
        d = request.POST.get('description')
        l = request.POST.get('location')
        s_d = request.POST.get('start_date')
        s_t = request.POST.get('start_time')
        e_d = request.POST.get('end_date')
        e_t = request.POST.get('end_time')
        
        repeat_event = True if request.POST.get('yes_repeat') == "on" else False
        
        # no_repeat = True if request.POST.get('no_repeat') == "on" else False
        # yes_repeat = True if request.POST.get('yes_repeat') == "on" else False

        r_e = False
        sun = False
        mon = False
        tue = False
        wed = False
        thu = False
        fri = False
        sat = False
        if repeat_event:
            r_e = True
            sun = True if request.POST.get('sunday') == "on" else False
            mon = True if request.POST.get('monday') == "on" else False
            tue = True if request.POST.get('tuesday') == "on" else False
            wed = True if request.POST.get('wednesday') == "on" else False
            thu = True if request.POST.get('thursday') == "on" else False
            fri = True if request.POST.get('friday') == "on" else False
            sat = True if request.POST.get('saturday') == "on" else False

        fresh_event = Event.objects.create(
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
            
        # create entries as appropriate
        creation_datetime = getTodayDateTime()
        # if repeat event, then make 30 days worth of entries for event
        if repeat_event:
            today_date = getTodayDate()
            loop_date = today_date
            
            
            # acceptable weekday values
            acceptable_weekdays = []
            if sun:
                acceptable_weekdays += [6]
            elif mon:
                acceptable_weekdays += [0]
            elif tue:
                acceptable_weekdays += [1]
            elif wed:
                acceptable_weekdays += [2]
            elif thu:
                acceptable_weekdays += [3]
            elif fri:
                acceptable_weekdays += [4]
            elif sat:
                acceptable_weekdays += [5]
            
            count = 0
            
            while count < 30:
                # is the loop_date on a weekday that matches the event's?
                loop_weekday = getWeekdayArray()[loop_date.weekday()]
                if loop_weekday in acceptable_weekdays:
                    EventEntry.objects.create(
                        event = fresh_event,
                        start_date = loop_date,
                        datetime_created = creation_datetime,
                        completed = False)
                    count += 1
                    print(count)
        else:
            EventEntry.objects.create(
                event = fresh_event,
                start_date = fresh_event.start_date,
                datetime_created = creation_datetime,
                completed = False)
                
                
                
            
            # for i in range(0,30):
            #     EventEntry.objects.create(
            #         event = fresh_event
            #         #start_date needs to be taken from an array
            #         start_date = 
            #         datetime_created = 
            #         completed = 
            #     )
            
        
            
        if add_another == "yes":
            x = {}
            x['success_message'] = "Event Added!"
            return render(request, 'main/add_event.html', x)
        
        
        # return render(request, 'main/event_list.html')
        return HttpResponseRedirect(reverse('main:event_list'))
        
    return render(request, 'main/add_event.html')

def add_multi_event(request):
    if request.method == 'POST':
        raw_data = request.POST.get('data')
        data = eval(raw_data)
        
        new_events = []
        for i in data:
            new_event = Event.objects.create(
                title = i[0],
                description = i[1],
                location = i[2],
                start_date = i[3],
                start_time = i[4],
                end_date = i[5],
                end_time = i[6],
                repeat_event = False,
                sunday = False,
                monday = False,
                tuesday = False,
                wednesday = False,
                thursday = False,
                friday = False,
                saturday = False)
            new_events += [new_event]
        x = {}
        x['success_message'] = "Events Added!"
        return render(request, 'main/add_multi_event.html', x)
    return render(request, 'main/add_multi_event.html')

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
    
def event_entry_detail(request, pk):
    
    certain_event_entry = EventEntry.objects.get(id=pk)
    x = {}
    x['certain_event_entry'] = certain_event_entry
    
    return render(request, 'main/event_entry_detail.html', x)
    
def week_agenda(request):
    today_date = getTodayDate()
    today_string = today_date.strftime("%Y-%m-%d")
    week_ahead_date = today_date + timedelta(days=7)
    week_ahead_string = week_ahead_date.strftime("%Y-%m-%d")
    
    week_event_entries = EventEntry.objects.filter(
        event__start_date__range=[today_string, week_ahead_string])
    
    l = []
    loop_date = today_date
    while loop_date < week_ahead_date:
        loop_weekday = getWeekdayArray()[loop_date.weekday()].capitalize()
        # list of event entries
        loop_event_entries = week_event_entries.filter(
            event__start_date = loop_date).order_by('event__start_date')
        
        l += [[loop_weekday,loop_event_entries]]
        loop_date += timedelta(days=1)
    
    x = {}
    x['l'] = l
    return render(request, 'main/week_agenda.html', x)

# Create your views here.
