from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from datetime import datetime, date, timedelta
from time import sleep
from django.db.models import Q

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
        s_d = request.POST.get('date')
        s_t = request.POST.get('start_time')
        e_t = request.POST.get('end_time')
        
        print(request.POST)
        
        repeat_event = True if request.POST.get('yes_repeat') == "on" else False
        
        print(1)
        
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
            
        print(sun,mon,tue,wed,thu,fri,sat)

        fresh_event = Event.objects.create(
            title = t,
            description = d,
            location = l,
            date = s_d,
            start_time = sanitize_time(s_t),
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
        print(3)
        # if repeat event, then make 30 days worth of entries for event
        if repeat_event:
            today_date = getTodayDate()
            loop_date = today_date
            
            
            # acceptable weekday values
            acceptable_weekdays = []
            if sun:
                acceptable_weekdays += [getWeekdayArray()[6]]
            if mon:
                acceptable_weekdays += [getWeekdayArray()[0]]
            if tue:
                acceptable_weekdays += [getWeekdayArray()[1]]
            if wed:
                acceptable_weekdays += [getWeekdayArray()[2]]
            if thu:
                acceptable_weekdays += [getWeekdayArray()[3]]
            if fri:
                acceptable_weekdays += [getWeekdayArray()[4]]
            if sat:
                acceptable_weekdays += [getWeekdayArray()[5]]
            print(acceptable_weekdays)
            
            count = 0
            print('enter loop...')
            while count < 30:
                # is the loop_date on a weekday that matches the event's?
                loop_weekday = getWeekdayArray()[loop_date.weekday()]
                print(loop_weekday)
                print('loop wd',loop_weekday,'days',acceptable_weekdays)
                if loop_weekday in acceptable_weekdays:
                    EventEntry.objects.create(
                        event = fresh_event,
                        date = loop_date)
                    count += 1
                print(count)
                loop_date += timedelta(days=1)
                # sleep(5)
            print('loop done')
        else:
            EventEntry.objects.create(
                event = fresh_event,
                date = fresh_event.date)
                
                
                
            
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
        creation_datetime = getTodayDateTime()
        raw_data = request.POST.get('data')
        data = eval(raw_data)
        
        new_events = []
        for i in data:
            new_event = Event.objects.create(
                title = i[0],
                description = i[1],
                location = i[2],
                date = i[3],
                start_time = i[4],
                end_time = i[6],
                repeat_event = False,
                sunday = False,
                monday = False,
                tuesday = False,
                wednesday = False,
                thursday = False,
                friday = False,
                saturday = False)
                
            EventEntry.objects.create(
                event = new_event,
                date = new_event.date,
                datetime_created = creation_datetime,
                completed = False)
            new_events += [new_event]
        x = {}
        x['success_message'] = "Events Added!"
        return render(request, 'main/add_multi_event.html', x)
    return render(request, 'main/add_multi_event.html')

# def today_agenda(request):
#     today = getTodayDateTime()
#     today_weekday = getWeekdayArray()[today.weekday()]
#     query1 = Q(**{today_weekday: True})
#     query2 = Q(start_date=today)
#     today_events = Event.objects.filter( query1 | query2 )
    
#     for event in today_events:
#         today_event_entries = EventEntry.objects.filter(
#             event = event,
#             datetime_created__year = today.year,
#             datetime_created__month = today.month,
#             datetime_created__day = today.day)
        
#         if len(today_event_entries) == 0:
#             event_entry = EventEntry.objects.create(
#                 event = event,
#                 datetime_created = today,
#                 completed = False,
#                 start_date = today)
                
#     routine_events = Event.objects.filter(repeat_event=True)
    

    
#     t = getTodayDate()
#     x = t - timedelta(days=365)
#     dates = []
#     while x <= t:
#         dates += [x]
#         x += timedelta(days=1)
        
#     all_event_entries = EventEntry.objects.all()
#     for event in routine_events:
#         weekday_list = []
        
#         if event.monday:
#             weekday_list += [0]
#         if event.tuesday:
#             weekday_list += [1]
#         if event.wednesday:
#             weekday_list += [2]
#         if event.thursday:
#             weekday_list += [3]
#         if event.friday:
#             weekday_list += [4]
#         if event.saturday:
#             weekday_list += [5]
#         if event.sunday:
#             weekday_list += [6]
#         relevant_dates = []
#         for date in dates:
#             if date.weekday() in weekday_list:
#                 same_entries = all_event_entries.filter(
#                     event = event,
#                     start_date = date)
#                 if len(same_entries) == 0:
#                     EventEntry.objects.create(
#                         event = event,
#                         datetime_created = today,
#                         completed = False,
#                         start_date = date)
#         print(relevant_dates)
            
        



#     x = {}
#     # x['event_entries'] = EventEntry.objects.filter(
#     #     datetime_created__year = today.year,
#     #     datetime_created__month = today.month,
#     #     datetime_created__day = today.day).order_by('event__start_time')
#     x['event_entries'] = EventEntry.objects.filter(
#         start_date = today).order_by('event__start_time')
    
#     return render(request, 'main/today_agenda.html', x)

def today_agenda(request):
    today_date = getTodayDate()
    today_weekday = getWeekdayArray()[today_date.weekday()]
    
    # today_nonroutine_event_entries
    query1 = Q(date = today_date)
    t_nr_e_e = EventEntry.objects.filter(query1)
    
    # today_routine_event_entries
    query2 = Q(**{'event__'+today_weekday:True})
    t_r_e_e = EventEntry.objects.filter(query1 & query2)
    
    # all_today_event_entries
    a_t_e_e = t_r_e_e | t_nr_e_e
    print(a_t_e_e)
    
    x = {}
    x['today_event_entries'] = a_t_e_e
    return render(request, 'main/today_agenda.html', x)
    
def tomorrow_agenda(request):
    tomorrow_date = getTodayDate() + timedelta(days=1)
    tomorrow_weekday = getWeekdayArray()[tomorrow_date.weekday()]
    
    # tomorrow_nonroutine_event_entries
    query1 = Q(date = tomorrow_date)
    t_nr_e_e = EventEntry.objects.filter(query1)
    
    # tomorrow_routine_event_entries
    query2 = Q(**{'event__'+tomorrow_weekday:True})
    t_r_e_e = EventEntry.objects.filter(query1 & query2)
    
    # all_tomorrow_event_entries
    a_t_e_e = t_r_e_e | t_nr_e_e
    
    x = {}
    x['tomorrow_event_entries'] = a_t_e_e
    return render(request, 'main/tomorrow_agenda.html', x)

    
def event_entry_detail(request, pk):
    
    certain_event_entry = EventEntry.objects.get(id=pk)
    x = {}
    x['certain_event_entry'] = certain_event_entry
    
    return render(request, 'main/event_entry_detail.html', x)
    
def week_agenda(request):
    weekday_array = getWeekdayArray()
    today_date = getTodayDate()
    today_string = today_date.strftime("%Y-%m-%d")
    week_ahead_date = today_date + timedelta(days=7)
    week_ahead_string = week_ahead_date.strftime("%Y-%m-%d")
    
    week_event_entries = EventEntry.objects.filter(
        event__date__range=[today_string, week_ahead_string])
    
    l = []
    loop_date = today_date
    while loop_date < week_ahead_date:
        loop_weekday = getWeekdayArray()[loop_date.weekday()]
        
        # loop_nonroutine_event_entries
        query1 = Q(date = loop_date)
        l_nr_e_e = EventEntry.objects.filter(query1)
        
        # loop_routine_event_entries
        query2 = Q(**{'event__'+loop_weekday:True})
        l_r_e_e = EventEntry.objects.filter(query1 & query2)
        
        # all_loop_event_entries
        a_l_e_e = l_r_e_e | l_nr_e_e
        
        l += [[loop_weekday.capitalize(),a_l_e_e]]
        loop_date += timedelta(days=1)
    
    x = {}
    x['l'] = l
    return render(request, 'main/week_agenda.html', x)

# Create your views here.
