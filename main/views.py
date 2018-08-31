from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')\
    
def event_list(request):
    return render(request, 'main/event_list.html')

# Create your views here.
