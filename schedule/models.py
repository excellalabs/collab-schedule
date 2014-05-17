from django.db import models
from django.contrib.auth import User

class time_away(models.Model):
	user = models.ForeignKey(User)
	date = models.DateField()