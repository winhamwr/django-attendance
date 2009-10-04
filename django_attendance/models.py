from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

from schedule.models import Occurrence

class Attendance(models.Model):
    '''
    The attendance status of a user for a specific Occurrence of an event.
    '''
    user = models.ForeignKey(User)
    occurrence = models.ForeignKey(Occurrence)
    attended = models.BooleanField(default=False)

    attendance_recorder = models.ForeignKey(User, related_name='recorded_attendances')
    attendance_recorded_date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = _('attendance')
        verbose_name_plural = _('attendances')

    def __unicode__(self):
        return "Attendance for %s at %s" % (self.user, self.occurrence)