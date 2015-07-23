from __future__ import print_function
from __future__ import unicode_literals

# python
import logging
import sys
import socket

# django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

# app
from sentinel.models import Event, Sentinel, id_generator, ContactInfo
from sentinel.forms import SentinelAddForm, SentinelEditForm, ContactInfoForm


logger = logging.getLogger('w4e')


def log_view(request, msg):
    hostname = socket.gethostname()
    hostname = hostname.replace('.local','')
    if request.user.is_anonymous():
        u = 'anonymous'
    else:
        u = request.user.username
    logger.info('{}:{} - view - {}'.format(hostname, u, msg))


def index(request):
    log_view(request, 'home_page')
    if request.user.is_anonymous():
        return TemplateView.as_view(template_name="index.html")(request)
    else:
        return redirect('/sentinels/list')


@login_required
def event_history(request):
    event_list = Event.recent(user=request.user)
    log_view(request, 'event_history - {}'.format(len(event_list)))
    return render(request, 'sentinel/events.html',
                  {'event_list': event_list})


@login_required
def list(request):
    stn_list = Sentinel.objects.filter(user=request.user)
    log_view(request, 'list_monitors - {}'.format(len(stn_list)))
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
            log_view(request, 'add_monitor - {}/{}'.format(stn.name, stn.tag))
            return redirect('/sentinels/list/')
    else:
        tag = id_generator()
        log_view(request, 'monitor_add_form')
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
            log_view(request, 'edited_monitor - {}'.format(stn.name))
            return redirect('/sentinels/list/')
    else:
        stn = Sentinel.objects.get(id=id)
        form = SentinelEditForm(instance=stn)
        url = 'http://watch4.events/checkin/{}/'.format(stn.tag)
        log_view(request, 'monitor_details - {}/{}'.format(stn.name, stn.tag))
        event_list = Event.objects.filter(tag=stn.tag).order_by('-time')
        # limit to 20
        event_list = event_list[:20]
        return render(request, 'sentinel/edit.html', {'form': form, 'id': id,
                                                      'tagURL': url, 'event_list': event_list})


@login_required
def delete(request, id):
    stn = get_object_or_404(Sentinel, id=id, user=request.user)
    log_view(request, 'delete - {}'.format(stn.name))
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
        log_view(request, 'set_contact_info - {}'.format(ci.contact_by))
        return redirect('/accounts/contact/')
    return render(request, 'registration/contact_info_form.html', {'form': form})


def checkin(request, tag):
    # make sure the url argument parsing did not leave spaces of trailing /
    tag = tag.strip('/ ')

    evt = Event.add_checkin(tag)
    log_view(request, 'checkin - {}'.format(tag))
    return render(request, 'sentinel/checkin.html', {'event': evt})
