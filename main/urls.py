from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^event_list/$', views.event_list, name='event_list'),
    url(r'^add_event/$', views.add_event, name='add_event'),
]