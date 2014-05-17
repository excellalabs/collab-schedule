from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class TimeAway(models.Model):
	user = models.ForeignKey(User)
	date = models.DateField()
	def get_absolute_url(self):
		return "time_away"