from django.views.generic import CreateView, TemplateView
from .models import TimeAway
from .forms import TimeAwayForm
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from core.models import Person

TEMPLATE_PATH = 'schedule/'

def _create_params(req):
    p = {'is_schedule': True, }
    p.update(csrf(req))
    return p

class TimeAwayView(CreateView):
	model = TimeAway
	form_class = TimeAwayForm

class CalendarView(TemplateView):
	template_name = "calendar.html"

@login_required
def time_away_list(req, stub):
    person = Person.objects.get(stub=stub)

    vacation_list = TimeAway.objects.filter(user=person.user)

    p = _create_params(req)
    p['vacation_list'] = vacation_list
    return render_to_response(TEMPLATE_PATH + "time_away_list.html", p,
                              context_instance=RequestContext(req))
