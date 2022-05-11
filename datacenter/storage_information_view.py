from django.utils.timezone import localtime

from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []
    for visit in visits:
        name = Passcard.objects.get(visit__entered_at=visit.entered_at)
        entered = localtime(visit.entered_at)
        duration = format_duration(get_duration(visit))
        visitor = {
            'who_entered': name,
            'entered_at': entered,
            'duration': duration
        }
        non_closed_visits.append(visitor)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)


def get_duration(visit):
    duration_time = localtime() - visit.entered_at
    return duration_time


def format_duration(duration_time):
    duration_formatted = str(duration_time).split('.')[0]
    return duration_formatted
