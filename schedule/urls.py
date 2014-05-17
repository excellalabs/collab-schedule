from django.conf.urls import patterns, url
from .views import TimeAwayView, CalendarView

urlpatterns = patterns('schedule.views',
                       url(r'^time_away$', TimeAwayView.as_view(), name='time_away'),
                       url(r'^calendar$', CalendarView.as_view(), name='calendar')
                       )
