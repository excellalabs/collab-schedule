from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class TimeAwayType(models.Model):
	code = models.CharField(max_length=30)

class TimeAway(models.Model):
	user = models.ForeignKey(User)
	date = models.DateField()
	type = models.ForeignKey(TimeAwayType)
	def get_absolute_url(self):
		return "time_away"