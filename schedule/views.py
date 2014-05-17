from django.views.generic import CreateView
from .models import time_away

class TimeAwayView(CreateView):
	model = time_away