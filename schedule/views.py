from django.views.generic import CreateView, TemplateView
from .models import TimeAway
from .forms import TimeAwayForm
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from core.models import Person
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from datetime import date
import json

TEMPLATE_PATH = 'schedule/'

def _create_params(req):
    p = {'is_schedule': True, }
    p.update(csrf(req))
    return p

class TimeAwayView(CreateView):
    model = TimeAway
    form_class = TimeAwayForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = Person.objects.get(user=self.request.user)
        obj.save()
        return super(TimeAwayView, self).form_valid(form)

    def get_success_url(self):
        person = Person.objects.get(user=self.request.user)
        return reverse("schedule:time_away_list", args=[person.stub])

class CalendarView(TemplateView):
    template_name = "calendar.html"

@login_required
def time_away_list(req, stub):
    person = Person.objects.get(stub=stub)

    vacation_list = TimeAway.objects.filter(user=person.user)
    vacation_list = vacation_list.filter(date__gte=date.today)
    vacation_list = vacation_list.order_by('date')[:10]

    p = _create_params(req)
    p['vacation_list'] = vacation_list
    return render_to_response(TEMPLATE_PATH + "time_away_list.html", p,
                              context_instance=RequestContext(req))

def calendar_json(req):
    json_list = []
    for entry in TimeAway.objects.all():
        id = entry.id
        if entry.type == 'AWA':
            title = entry.user.user.last_name + " - AWA"
        elif entry.type == 'AWAY':
            title = entry.user.user.last_name + " - OOO"
        start = entry.date.strftime("%Y-%m-%dT%H:%M:%S")
        allDay = True

        json_entry = {'id':id, 'start':start, 'allDay':allDay, 'title': title}
        json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='application/json')
