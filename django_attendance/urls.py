from django.conf.urls.defaults import *

urlpatterns = patterns('django_attendance.views',

# Already-persisted occurrence
url(r'^(?P<occurrence_id>\d+)/$',
    'attendance',
    name="attendance_attendance_view"),

url(r'^(?P<occurrence_id>\d+)/signup/$',
    'signup',
    name="attendance_signup"),

# Non-persisted occurrence
url(r'^(?P<event_id>\d+)/(?P<iso_date>[-:\w]+)/signup/$',
    'signup_by_iso_date',
    name="attendance_signup_by_iso_date"),

# Reports
url(r'^mine/$',
    'user_attendance',
    name="attendance_mine"),
url(r'^user/(?P<user_id>\d+)/report/$',
    'user_attendance',
    name="attendance_for_user"),
url(r'^user/report/$',
    'attendance_by_user',
    name="attendance_by_user"),

)