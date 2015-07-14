from __future__ import print_function
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
from sentinel.models import Event, Sentinel, id_generator, ContactInfo
from sentinel.forms import SentinelAddForm, SentinelEditForm, ContactInfoForm

from django.utils import timezone
import sys


def event_history(request):
    event_list = Event.recent()
    return render(request, 'sentinel/events.html',
                  {'event_list': event_list})


@login_required
def list(request):
    stn_list = Sentinel.objects.filter(user=request.user)
    for stn in stn_list:
        stn.num_ci = Event.objects.filter(tag=stn.tag).count()
    return render(request, 'sentinel/list.html', {'wl': stn_list})


@login_required
def add(request):
    if request.method == 'POST':
        form = SentinelAddForm(request.POST)
        tag = form['tag'].value()
        if form.is_valid():
            stn = form.save(commit=False)
            stn.user = request.user
            stn.save()
            return redirect('/sentinels/list/')
    else:
        tag = id_generator()
        form = SentinelAddForm(initial={'tag': tag})
    url = 'http://watch4.events/checkin/{}/'.format(tag)
    return render(request, 'sentinel/add.html', {'form': form,
                                                 'tagURL': url})


@login_required
def edit(request, id):
    if request.method == 'POST':
        stn = Sentinel.objects.get(id=id)
        form = SentinelEditForm(request.POST, instance=stn)
        if form.is_valid():
            form.save()
            return redirect('/sentinels/list/')
    else:
        stn = Sentinel.objects.get(id=id)
        form = SentinelEditForm(instance=stn)
        url = 'http://watch4.events/checkin/{}/'.format(stn.tag)
        event_list = Event.objects.filter(tag=stn.tag).order_by('-time')
        # limit to 20
        event_list = event_list[:20]
        return render(request, 'sentinel/edit.html', {'form': form, 'id': id,
                                                      'tagURL': url, 'event_list': event_list})


@login_required
def delete(request, id):
    stn = get_object_or_404(Sentinel, id=id, user=request.user)
    stn.delete()
    return redirect('/sentinels/list/')


# def detail(request, id):
#     stn = get_object_or_404(Sentinel, id=id)
#     event_list = Event.objects.filter(tag=stn.tag)
#     return render(request, 'sentinel/details.html',
#                   {'stn': stn, 'event_list': event_list})

@login_required
def contact(request):
    user = request.user
    try:
        ci = ContactInfo.objects.get(user=user)
    except:
        ci = ContactInfo(user=user, email=user.email)
        ci.save()

    # seems to be proper way to handle get or post request
    form = ContactInfoForm(request.POST or None, instance=ci)

    if request.method == 'POST' and form.is_valid():
        print('saved user form', file=sys.stderr)
        ci = form.save()
        return redirect('/accounts/contact/')
    return render(request, 'registration/contact_info_form.html', {'form': form})


def checkin(request, tag):
    now = timezone.now()
    # make sure the url argument parsing did not leave spaces of trailing /
    tag = tag.strip('/ ')
    e = Event(tag=tag, log_type=Event.LOG, time=now)
    e.save()
    return render(request, 'sentinel/checkin.html', {'tag': tag, 'now': now})
