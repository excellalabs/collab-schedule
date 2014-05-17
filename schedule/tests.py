from django.test import TestCase
from django.core.urlresolvers import reverse

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
