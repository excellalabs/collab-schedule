from django.test import TestCase
from django.core.urlresolvers import reverse

class TimeAwayTest(TestCase):

    fixtures = ['core-test-fixtures', ]

    def test_add_time_away_without_user_login(self):
    	response = self.client.get(reverse('schedule:time_away'))
    	self.assertEquals(302, response.status_code)

    def test_add_time_away_with_user_login(self):
    	self.client.login(username='test1@example.com', password='1')
    	response = self.client.get(reverse('schedule:time_away'))
    	self.assertEquals(200, response.status_code)
