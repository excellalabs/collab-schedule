from django.db import models
from django.contrib.auth.models import User

class time_away(models.Model):
	user = models.ForeignKey(User)
	date = models.DateField()
