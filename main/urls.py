from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^event_list/$', views.event_list, name='event_list'),
    url(r'^add_event/$', views.add_event, name='add_event'),
    url(r'^add_multi_event/$', views.add_multi_event, name='add_multi_event'),
    url(r'^today_agenda/$', views.today_agenda, name='today_agenda'),
    url(r'^tomorrow_agenda/$', views.tomorrow_agenda, name='tomorrow_agenda'),
    url(r'^week_agenda/$', views.week_agenda, name='week_agenda'),
    url(r'^delete_event_entry/(?P<pk>[0-9]+)/$', views.delete_event_entry, name='delete_event_entry'),

    url(r'^event_entry_detail/(?P<pk>[0-9]+)/$', views.event_entry_detail, name='event_entry_detail'),
]