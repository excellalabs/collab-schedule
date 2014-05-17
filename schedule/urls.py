from django.conf.urls import patterns, url
from .views import TimeAwayView, CalendarView

urlpatterns = patterns('schedule.views',
                       url(r'^time_away$', TimeAwayView.as_view(), name='time_away'),
                       url(r'^time_away_list/(?P<stub>.*)/', 'time_away_list', name='time_away_list'),
                       url(r'^calendar$', CalendarView.as_view(), name='calendar')
                       )
