from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^event_list/$', views.event_list, name='event_list'),
    url(r'^add_event/$', views.add_event, name='add_event'),
    url(r'^today_agenda/$', views.today_agenda, name='today_agenda'),
    url(r'^event_entry_detail/(?P<pk>[0-9]+)/$', views.event_entry_detail, name='event_entry_detail'),
]