from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import TimeAwayType

class ScheduleTest(TestCase):

    def test_vacation_list_user_with_vacation(self):
        response = self.client.get(reverse('schedule:list'))
        self.assertEquals(200, response.status_code)

    def test_vacation_list_user_without_vacation(self):
        response = self.client.get(reverse('schedule:list'))
        self.assertEquals(200, response.status_code)

    def test_vacation_list_invalid_user(self):
        response = self.client.get(reverse('schedule:list'))
        self.assertEquals(404, response.status_code)

    def test_timeAwayType_list_returns_all(self):
        # Arrange
		a = TimeAwayType.objects.create(code='Away')
		
		# Act
		result = TimeAwayType.objects.all()
		
		# Assert
		self.assertIn(a, result)