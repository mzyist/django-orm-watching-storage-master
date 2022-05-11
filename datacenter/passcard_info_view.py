from django.utils.timezone import localtime

from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def get_duration(visit):
    if visit.leaved_at:
        duration_time = localtime(visit.leaved_at) - visit.entered_at
    else:
        duration_time = localtime() - visit.entered_at
    return duration_time


def format_duration(duration_time):
    duration_formatted = str(duration_time).split('.')[0]
    return duration_formatted


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    duration_seconds = duration.seconds
    sus_seconds = minutes * 60
    if duration_seconds < sus_seconds:
        return False
    else:
        return True


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.all()[0]
    this_passcard_visits = []
    passcard_visits = Visit.objects.filter(passcard__owner_name=passcard)
    for visit in passcard_visits:
        flag = is_visit_long(visit)
        entered = localtime(visit.entered_at)
        duration = format_duration(get_duration(visit))
        visitor = {
            'entered_at': entered,
            'duration': duration,
            'is_strange': flag
        }
        this_passcard_visits.append(visitor)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
