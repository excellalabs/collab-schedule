from django.test import TestCase
from django.core.urlresolvers import reverse
from schedule.models import TimeAway
from datetime import date, timedelta
from core.models import Person

class VacationListTest(TestCase):

    fixtures = ['core-test-fixtures', ]

    def test_vacation_list_user_today(self):
        self.client.login(username='test1@example.com', password='1')
        user = Person.objects.get(user_id=1)

        today = date.today()
        vacation = TimeAway(user=user, date=today, type=TimeAway.OOO)
        vacation.save()

        response = self.client.get(reverse('schedule:time_away_list', args=('test1',)))
        self.assertEquals(200, response.status_code)
        self.assertContains(response, today.strftime("%d, %Y"))

    def test_vacation_list_yesterday(self):
        self.client.login(username='test1@example.com', password='1')
        user = Person.objects.get(user_id=1)

        yesterday=date.today()-timedelta(days=1)
        vacation = TimeAway(user=user, date=yesterday, type=TimeAway.OOO)
        vacation.save()

        response = self.client.get(reverse('schedule:time_away_list', args=('test1',)))
        self.assertNotContains(response, yesterday.strftime("%d, %Y"))

    def test_vacation_list_tomorrow(self):
        self.client.login(username='test1@example.com', password='1')
        user = Person.objects.get(user_id=1)

        tomorrow=date.today()+timedelta(days=1)
        vacation = TimeAway(user=user, date=tomorrow, type=TimeAway.OOO)
        vacation.save()

        response = self.client.get(reverse('schedule:time_away_list', args=('test1',)))
        self.assertContains(response, tomorrow.strftime("%d, %Y"))

    def test_vacation_list_user_without_vacation(self):
        self.client.login(username='test1@example.com', password='1')
        response = self.client.get(reverse('schedule:time_away_list', args=('test1',)))
        self.assertEquals(200, response.status_code)

    def test_vacation_list_login_required(self):
        response = self.client.get(reverse('schedule:time_away_list', args=('test1',)))
        self.assertEquals(302, response.status_code)
