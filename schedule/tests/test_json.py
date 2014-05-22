from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from schedule.models import TimeAway
from datetime import date, timedelta, datetime
import time
from core.models import Person
from schedule.views import calendar_json
import json

class JsonTest(TestCase):

    fixtures = ['core-test-fixtures', ]

    def test_json_all(self):
        user = Person.objects.get(user_id=1)
        user2 = Person.objects.get(user_id=3)

        today = date.today()
        future = date.today() + timedelta(days=400)
        past = date.today() - timedelta(days=5000)
        TimeAway.objects.create(user=user, date=today, type=TimeAway.OOO)
        TimeAway.objects.create(user=user2, date=future, type=TimeAway.AWA)
        TimeAway.objects.create(user=user, date=past, type=TimeAway.AWA)

        json_results = self.client.get(reverse('schedule:calendar_json'))
        data = json.loads(json_results.content)
        self.assertEqual(len(data), 3)

    def test_json_type(self):
        user = Person.objects.get(user_id=1)

        today = date.today()
        TimeAway.objects.create(user=user, date=today, type=TimeAway.OOO)
        TimeAway.objects.create(user=user, date=today, type=TimeAway.AWA)

        json_results = self.client.get(reverse('schedule:calendar_json'), {'type':'AWA'})
        data = json.loads(json_results.content)
        self.assertEqual(len(data), 1)
        self.assertIn('AWA', data[0]['title'])

    def test_json_start_date(self):
        user = Person.objects.get(user_id=1)

        today = date.today()
        now = time.mktime(datetime.now().timetuple())
        future = date.today() + timedelta(days=1)
        past = date.today() - timedelta(days=1)
        TimeAway.objects.create(user=user, date=today, type=TimeAway.OOO)
        TimeAway.objects.create(user=user, date=future, type=TimeAway.OOO)
        TimeAway.objects.create(user=user, date=past, type=TimeAway.OOO)

        json_results = self.client.get(reverse('schedule:calendar_json'), {'start':now})
        data = json.loads(json_results.content)
        self.assertEqual(len(data), 2)
        self.assertIn(today.strftime("%Y-%m-%dT%H:%M:%S"), [data[0]['start'], data[1]['start']])
        self.assertIn(future.strftime("%Y-%m-%dT%H:%M:%S"), [data[0]['start'], data[1]['start']])
        self.assertNotIn(past.strftime("%Y-%m-%dT%H:%M:%S"), [data[0]['start'], data[1]['start']])

    def test_json_end_date(self):
        user = Person.objects.get(user_id=1)

        today = date.today()
        now = time.mktime(datetime.now().timetuple())
        future = date.today() + timedelta(days=1)
        past = date.today() - timedelta(days=1)
        TimeAway.objects.create(user=user, date=today, type=TimeAway.OOO)
        TimeAway.objects.create(user=user, date=future, type=TimeAway.OOO)
        TimeAway.objects.create(user=user, date=past, type=TimeAway.OOO)

        json_results = self.client.get(reverse('schedule:calendar_json'), {'end':now})
        data = json.loads(json_results.content)
        self.assertEqual(len(data), 2)
        self.assertIn(today.strftime("%Y-%m-%dT%H:%M:%S"), [data[0]['start'], data[1]['start']])
        self.assertNotIn(future.strftime("%Y-%m-%dT%H:%M:%S"), [data[0]['start'], data[1]['start']])
        self.assertIn(past.strftime("%Y-%m-%dT%H:%M:%S"), [data[0]['start'], data[1]['start']])
