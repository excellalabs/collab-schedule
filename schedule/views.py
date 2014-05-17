from django.views.generic import CreateView, TemplateView
from .models import TimeAway
from .forms import TimeAwayForm

class TimeAwayView(CreateView):
	model = TimeAway
	form_class = TimeAwayForm

class CalendarView(TemplateView):
	template_name = "calendar.html"