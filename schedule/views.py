from django.views.generic import CreateView, TemplateView
from .models import time_away

class TimeAwayView(CreateView):
	model = time_away

class CalendarView(TemplateView):
	template_name = "calendar.html"