from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

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
        
        
        
        # 18:37 from mobile
        # 2:00am from desktop
        
        
        

        sanitize_time(s_t)
        sanitize_time(e_t)
        
        Event.objects.create(
            title = t,
            description = d,
            location = l,
            start_date = s_d,
            start_time = s_t,
            end_date = e_d,
            end_time = e_t,
            repeat_event = False,
            sunday = False,
            monday = False,
            tuesday = False,
            wednesday = False,
            thursday = False,
            friday = False,
            saturday = False)
        
        # return render(request, 'main/event_list.html')
        return HttpResponseRedirect(reverse('main:event_list'))
        
    return render(request, 'main/add_event.html')

# Create your views here.
