from django.db import models
from django.core.urlresolvers import reverse
from core.models import Person

class TimeAwayType(models.Model):
	code = models.CharField(max_length=30)

class TimeAway(models.Model):
	user = models.ForeignKey(Person)
	date = models.DateField()
	type = models.ForeignKey(TimeAwayType, null=True, blank=True)
	def get_absolute_url(self):
		return reverse("schedule:time_away")
