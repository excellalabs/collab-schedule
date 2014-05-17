from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class TimeAway(models.Model):
	TIME_AWAY_TYPES = (
		('AWA', 'Alternate Work Arrangement'),
		('AWAY', 'Away')
	)
	user = models.ForeignKey(User)
	date = models.DateField()
	type = models.CharField(max_length=4, choices=TIME_AWAY_TYPES, default='AWAY')
	def get_absolute_url(self):
		return "time_away"