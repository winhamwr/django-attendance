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
    attendee_statuses = models.ManyToManyField(User, through='AttendanceStatus')

    class Meta:
        verbose_name = _('attendance')
        verbose_name_plural = _('attendances')

    def __unicode__(self):
        return "Attendance for %s-%s" % (self.occurrence.title,
                                         self.occurrence.start)


class AttendanceStatus(models.Model):
    event_attendance = models.ForeignKey(EventAttendance)
    user = models.ForeignKey(User)
    attended = models.BooleanField(default=False)

    attendance_recorded_date = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return "Attendance status for %s at %s-%s" % (self.user,
                                                      self.event_attendance.occurrence.title,
                                                      self.event_attendance.occurrence.start)

class AttendanceStatusInline(admin.StackedInline):
    model = AttendanceStatus
    exclude = ('attendance_recorded_date',)
    extra = 5

class EventAttendanceAdmin(admin.ModelAdmin):
    inlines = [AttendanceStatusInline]


admin.site.register(EventAttendance, EventAttendanceAdmin)
