import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import permission_required, login_required

from schedule.models import Occurrence, Calendar
from schedule.views import get_occurrence

from django_attendance.models import EventAttendance

@login_required
def attendance(request, occurrence_id, template_name='django_attendance/attendance.html'):
    occurrence = get_object_or_404(Occurrence, pk=occurrence_id)
    try:
        ea = occurrence.eventattendance
    except EventAttendance.DoesNotExist:
        ea = EventAttendance(occurrence=occurrence)
        ea.save()

    attendees = ea.attendees.all().order_by('last_name')
    context = RequestContext(request, {'occurrence': occurrence,
                                       'attendees': attendees})

    return render_to_response(template_name, context)

@login_required
def user_attendance(request, user_id=None, template_name='django_attendance/user_attendance.html'):
    """
    An attendance report for a specific user. Displays the hours for a given user
    broken down by event with summaries.
    """
    if user_id:
        attendee = get_object_or_404(User, pk=user_id)
    else:
        attendee = request.user

    # 3-tuple of (calendar, occurrences and total_hours)
    cal_data = []
    for calendar in Calendar.objects.all():
        attended_occurrences = Occurrence.objects.filter(eventattendance__attendees=attendee, event__calendar=calendar).select_related('eventattendance').order_by('start')
        total_hours = sum([a.eventattendance.duration() for a in attended_occurrences])
        if total_hours > 0:
            cal_data.append((calendar, attended_occurrences, total_hours))

    context = RequestContext(request, dict(
        cal_data=cal_data,
        attendee=attendee
    ))

    return render_to_response(template_name, context)

@login_required
def attendance_by_user(request, template_name='django_attendance/attendance_by_user.html'):
    """
    An attendance report for a specific user. Displays the hours for a given user
    broken down by event with summaries.
    """
    # 3-tuple of (calendar, occurrences, user_hours)
    # ``user_hours`` is a 3-tuple of (user, [hours], total_hours) where hours is a ordered list
    # of the hours for that user in the corresponding occurrences
    cal_data = []
    for calendar in Calendar.objects.all():
        attended_occurrences = Occurrence.objects.filter(
            event__calendar=calendar).exclude(
                eventattendance__attendees__isnull=True).select_related(
                    'eventattendance').order_by('start')

        user_hours = []
        for attendee in User.objects.all():
            user_attended_occurrences = attended_occurrences.filter(eventattendance__attendees=attendee)
            total_hours = sum([a.eventattendance.duration() for a in user_attended_occurrences])
            if total_hours > 0:
                hours = []
                for o in attended_occurrences:
                    if o in user_attended_occurrences:
                        hours.append(o.eventattendance.duration())
                    else:
                        hours.append(0)

                user_hours.append((attendee, hours, total_hours))
        cal_data.append((calendar, attended_occurrences, user_hours))

    context = RequestContext(request, dict(
        cal_data=cal_data
    ))

    return render_to_response(template_name, context)



@permission_required('django_attendance.change_eventattendance')
def signup(request, occurrence_id, template_name='django_attendance/signup.html'):
    """
    A signup page where site members can enter their username and password and
    be marked as attending the event.
    """
    occurrence = get_object_or_404(Occurrence, pk=occurrence_id)

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Sign this user up
            ea, created = EventAttendance.objects.get_or_create(occurrence=occurrence)
            ea.save()
            ea.attendees.add(user)

            request.user.message_set.create(message="User %s %s successfully signed up" % (user.first_name, user.last_name))

            return HttpResponseRedirect(reverse('attendance_signup', kwargs={'occurrence_id':occurrence.pk}))
    else:
        form = AuthenticationForm(request)

    context = RequestContext(request, {'form':form})

    return render_to_response(template_name, context)

def signup_by_iso_date(request, event_id, iso_date):
    """
    Make a signup for an occurrence that hasn't yet been persisted.
    """
    t = datetime.datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S")
    event, occurrence = get_occurrence(event_id, year=t.year, month=t.month,
                                       day=t.day, hour=t.hour,
                                       minute=t.minute, second=t.second)
    occurrence.save()

    return signup(request, occurrence.pk)