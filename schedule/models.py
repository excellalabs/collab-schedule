from django.db import models
from django.core.urlresolvers import reverse
from core.models import Person

class TimeAway(models.Model):
    AWA = 'AWA'
    OOO = 'OOO'

    TIME_AWAY_TYPES = (
        (AWA, 'Alternate Work Arrangement'),
        (OOO, 'Out of Office')
    )
    user = models.ForeignKey(Person)
    date = models.DateField()
    type = models.CharField(max_length=4, choices=TIME_AWAY_TYPES, default=OOO)
    def get_absolute_url(self):
        return reverse("schedule:time_away")
