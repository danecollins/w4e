from __future__ import print_function
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from sentinel.models import Event, Sentinel, id_generator
from sentinel.forms import SentinelAddForm, SentinelEditForm
from django.utils import timezone
import sys


def event_history(request):
    event_list = Event.recent()
    return render(request, 'sentinel/events.html',
                  {'event_list': event_list})


def list(request):
    stn_list = Sentinel.objects.all()
    return render(request, 'sentinel/list.html', {'wl': stn_list})


def add(request):
    if request.method == 'POST':
        form = SentinelAddForm(request.POST)
        if form.is_valid():
            stn = form.save(commit=False)
            stn.save()
            return redirect('/sentinel/list/')
    else:
        form = SentinelAddForm(initial={'tag': id_generator()})
        return render(request, 'sentinel/add.html', {'form': form})

def edit(request, id):
    if request.method == 'POST':
        stn = Sentinel.objects.get(id=id)
        form = SentinelEditForm(request.POST, instance=stn)
        if form.is_valid():
            form.save()
            return redirect('/sentinel/list/')
    else:
        stn = Sentinel.objects.get(id=id)
        form = SentinelEditForm(instance=stn)
        return render(request, 'sentinel/edit.html', {'form': form, 'id': id})


def detail(request, id):
    stn = get_object_or_404(Sentinel, id=id)
    event_list = Event.objects.filter(tag=stn.tag)
    return render(request, 'sentinel/details.html',
                  {'stn': stn, 'event_list': event_list})


def checkin(request, tag):
    e = Event(tag=tag, log_type=Event.LOG, time=timezone.now())
    e.save()
    return render(request, 'sentinel/checkin.html',
                  {'tag': tag})
