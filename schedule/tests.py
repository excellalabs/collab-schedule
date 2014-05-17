from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import TimeAwayType, TimeAway
from django.contrib.auth.models import User
from datetime import date
from core.models import Person

class ScheduleTest(TestCase):

    fixtures = ['core-test-fixtures', ]

    def test_vacation_list_user_with_vacation(self):
        self.client.login(username='test1@example.com', password='1')
        user = User.objects.get(username='test1@example.com')
        vacation = TimeAway(user=user, date=date.today())
        vacation.save()

        response = self.client.get(reverse('schedule:time_away_list', args=('test1',)))
        self.assertEquals(200, response.status_code)

    def test_vacation_list_user_without_vacation(self):
        self.client.login(username='test1@example.com', password='1')
        response = self.client.get(reverse('schedule:time_away_list', args=('test1',)))
        self.assertEquals(200, response.status_code)

    def test_timeAwayType_list_returns_all(self):
        # Arrange
		a = TimeAwayType.objects.create(code='Away')
		
		# Act
		result = TimeAwayType.objects.all()
		
		# Assert
		self.assertIn(a, result)

    def test_vacation_list_login_required(self):
        response = self.client.get(reverse('schedule:time_away_list', args=('test1',)))
        self.assertEquals(302, response.status_code)
