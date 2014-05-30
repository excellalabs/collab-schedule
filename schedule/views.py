from django.views.generic import CreateView, TemplateView
from .models import TimeAway
from .forms import TimeAwayForm
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from core.models import Person
from core.taggit.models import TaggedItem
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from datetime import date, datetime
from django.db.models import Q
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

    def get_context_data(self, **kwargs):
        context = super(TimeAwayView, self).get_context_data(**kwargs)
        context['is_schedule'] = True
        return context

    def get_success_url(self):
        person = Person.objects.get(user=self.request.user)
        return reverse("schedule:time_away_list", args=[person.stub])

class CalendarView(TemplateView):
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)
        # TODO cleanup/optimize this mess of queries
        context['is_schedule'] = True
        context['projects'] = [ti.tag.slug for ti in Person.objects.get(user=self.request.user).tagged_items.filter(tag_category__slug='staff-directory-my-projects')]
        selected_projects = self.request.GET.get('projects', '').split(',')
        context['selected_projects'] = set(selected_projects).intersection(context['projects'])
        selected_projects_persons_id_list = [ti.object_id for ti in TaggedItem.objects.filter(tag_category__slug='staff-directory-my-projects', tag__slug__in=context['selected_projects']).exclude(object_id=Person.objects.get(user=self.request.user).id)]
        context['selected_projects_persons'] = Person.objects.filter(id__in=selected_projects_persons_id_list)
        context['user'] = self.request.user
        return context

@login_required
def time_away_list(req, stub=None):
    if stub:
        person = Person.objects.get(stub=stub)
    else:
        person = Person.objects.get(user=req.user)

    vacation_list = TimeAway.objects.filter(user=person)
    vacation_list = vacation_list.filter(date__gte=date.today)
    vacation_list = vacation_list.order_by('date')[:10]

    p = _create_params(req)
    p['person'] = person
    p['vacation_list'] = vacation_list
    return render_to_response(TEMPLATE_PATH + "time_away_list.html", p,
                              context_instance=RequestContext(req))

def calendar_json(req):
    json_list = []
    person = Person.objects.get(user_id=req.GET.get('user_id'))
    start_date = req.GET.get('start', None)
    end_date = req.GET.get('end', None)
    data_type = req.GET.get('type', None)
    project = req.GET.get('project', '__personal__')

    filter_query = Q()
    if start_date:
        filter_query = filter_query&Q(date__gte=datetime.fromtimestamp(int(float(start_date))))
    if end_date:
        filter_query = filter_query&Q(date__lte=datetime.fromtimestamp(int(float(end_date))))
    if data_type:
        filter_query = filter_query&Q(type=data_type)

    if project == '__personal__':
        filter_query = filter_query&Q(user=person)
    else:
        user_ids = [ti.object_id for ti in TaggedItem.objects.filter(tag_category__slug='staff-directory-my-projects', tag__slug=project)]
        filter_query = filter_query&Q(user__in=user_ids)
        filter_query = filter_query&~Q(user=person)

    for entry in TimeAway.objects.filter(filter_query):
        id = entry.id
        if entry.type == TimeAway.AWA:
            title = entry.user.user.last_name + " - AWA"
        elif entry.type == TimeAway.OOO:
            title = entry.user.user.last_name + " - OOO"
        start = entry.date.strftime("%Y-%m-%dT%H:%M:%S")
        allDay = True

        json_entry = {'id':id, 'start':start, 'allDay':allDay, 'title': title}
        json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='application/json')
