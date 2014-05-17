from django.db import models
from django.contrib.auth.models import User

class TimeAway(models.Model):
	user = models.ForeignKey(User)
	date = models.DateField()
	def get_absolute_url(self):
		return "/schedule/time_away"