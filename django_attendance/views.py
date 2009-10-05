import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse

from schedule.models import Occurrence
from schedule.views import get_occurrence

from django_attendance.models import EventAttendance

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

def signup(request, occurrence_id, template_name='django_attendance/signup.html'):
    """
    A signup page where site members can enter their username and password and
    be marked as attending the event.
    """
    context = RequestContext(request)

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