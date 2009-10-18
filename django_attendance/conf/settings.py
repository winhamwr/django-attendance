from django.conf import settings

# When determining the number of hours, real hours are multiplied by this number
# to give attendance hours. This is useful for organization that have rules like
# 50 minutes is one hour for attendance purposes, which gives a 1.2 multiplier.
HOUR_MULTIPLIER = getattr(settings, 'ATTENDANCE_HOUR_MULTIPLIER', 1)