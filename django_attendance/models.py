import datetime

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib import admin

from schedule.models import Occurrence

from django_attendance.conf import settings as attendance_settings

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

    def duration(self):
        """
        Get the duration of this event in hours, taking the HOUR_MULTIPLIER in
        to account.
        """
        delta = self.occurrence.end - self.occurrence.start
        real_hours = delta.days * 24 + delta.seconds / (60.0 * 60.0)

        adjusted_hours = attendance_settings.HOUR_MULTIPLIER * real_hours

        return adjusted_hours


admin.site.register(EventAttendance)
