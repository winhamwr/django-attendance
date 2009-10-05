import datetime

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib import admin

from schedule.models import Occurrence

class EventAttendance(models.Model):
    '''
    The attendance status of a user for a specific Occurrence of an event.
    '''
    occurrence = models.OneToOneField(Occurrence)
    attendees = models.ManyToManyField(User)

    class Meta:
        verbose_name = _('attendance')
        verbose_name_plural = _('attendances')

    def __unicode__(self):
        return "Attendance for %s-%s" % (self.occurrence.title,
                                         self.occurrence.start)


admin.site.register(EventAttendance)
