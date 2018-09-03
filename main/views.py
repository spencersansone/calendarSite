from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

def getTodayDateTime():
    return datetime.now()
    
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
            print("{}:{}".format(hour,minute))
            return "{}:{}".format(hour,minute)
    
    
    
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
        e_d = request.POST.get('end_date')
        print(e_d)
        e_t = request.POST.get('end_time')
        print(e_t)
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
    
# def today_agenda(request):
#     today = getTodayDateTime()
#     today_weekday = getWeekdayArray()[today.weekday()]
#     query1 = Q(**{today_weekday: True})
#     query2 = Q(date=today)
#     today_events = Event.objects.filter( query1 | query2 )
    

# Create your views here.
