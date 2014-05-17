from django.contrib import admin
from .models import TimeAwayType, TimeAway

admin.site.register(TimeAway)
admin.site.register(TimeAwayType)