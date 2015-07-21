from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail

import string
import random
import pytz
import datetime

import sys

utc = pytz.timezone('UTC')
from django.utils import timezone


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# ############################################################################## SENTINEL
class Sentinel(models.Model):
    name = models.CharField(max_length=50)
    tag = models.CharField(max_length=8)
    freq = models.IntegerField()
    user = models.ForeignKey(User)
    active = models.BooleanField(default=True, blank=True)

    def missed_checkin(self, test=False, debug=False):
        grace_period = 2  # minutes

        # skip inactive and never checked in
        if self.active and Event.objects.filter(sentinel=self).exists():
            delta = datetime.timedelta(hours=self.freq, minutes=grace_period)
            if test:
                expected = test - delta
            else:
                expected = timezone.now() - delta

            if debug:
                print('Working on {}'.format(self))
                print('   expected = {}'.format(expected))

            # get last checkin
            last = Event.objects.filter(sentinel=self).order_by('-id')[0]
            if debug:
                print('   last = {}'.format(last))
            if last.log_type == Event.LOG:
                if last.time < expected:
                    if debug:
                        print('   missed event')
                    return last
            else:
                # already notified on this
                if debug:
                    print('   already notified')
                return False

        else:
            if debug:
                print('Skipping {!r} because inactive'.format(self))
            return False

    def __str__(self):
        return 'Sentinel({},{},{},{},{})'.format(self.name,
                                                 self.user,
                                                 self.tag,
                                                 self.freq,
                                                 self.active)

    def __repr__(self):
        return "Sentinel(name='{}', tag='{}', freq={}, active={})".format(self.name,
                                                                          self.tag,
                                                                          self.freq,
                                                                          self.active)


# ################################################################################# EVENT
class Event(models.Model):
    LOG = 'LOG'
    NOTIFICATION = 'NOT'
    TYPE_CHOICES = (
        (LOG, 'Log'),
        (NOTIFICATION, 'Notification')
    )
    time = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=30)
    sentinel = models.ForeignKey(Sentinel)
    log_type = models.CharField(max_length=3,
                                choices=TYPE_CHOICES,
                                default=LOG)

    @classmethod
    def add_event(cls, tag, type):
        s = Sentinel.objects.get(tag=tag)
        e = cls(tag=tag, sentinel=s, log_type=type)
        e.save()
        return e

    @classmethod
    def add_checkin(cls, tag):
        return cls.add_event(tag, cls.LOG)

    @classmethod
    def add_notification(cls, tag):
        return cls.add_event(tag, cls.NOTIFICATION)

    @classmethod
    def recent(self, user=False):
        if user:
            events = Event.objects.filter(sentinel__user=user).order_by('-id')[:30]
        else:
            events = Event.objects.all().order_by('-id')[:30]

        tags = set([x.tag for x in events])
        tag_name = {tag: Sentinel.objects.get(tag=tag).name for tag in tags}
        event_list = []
        for e in events:
            e.name = tag_name[e.tag]
            event_list.append(e)
        return event_list

    @classmethod
    def fix_db(cls):
        i = 0
        for obj in cls.objects.all():
            s = Sentinel.objects.get(tag=obj.tag)
            if s != obj.sentinel:
                obj.sentinel = s
                obj.save()
                i += 1

        return i  # objects fixed

    def __str__(self):
        tm = self.time.astimezone(utc)
        time_str = tm.strftime('%h-%d %H:%M')
        return '<Event: {},{},{}>'.format(self.tag,
                                          time_str,
                                          self.log_type)

    def __repr__(self):
        return 'Event({},{},{})'.format(self.tag, self.time, self.log_type)


# ############################################################################## CONTACT
class ContactInfo(models.Model):
    SMS = 'SMS'
    EMAIL = 'EMAIL'
    CONTACT_CHOICES = (
        (SMS, 'SMS'),
        (EMAIL, 'Email')
    )
    user = models.OneToOneField(User, primary_key=True)
    contact_by = models.CharField(max_length=5, choices=CONTACT_CHOICES, default=EMAIL)
    email = models.CharField(max_length=40, blank=True)
    number = models.CharField(max_length=16, blank=True)

    @classmethod
    def create_default(cls, user):
        ci = cls(user=user, email=user.email)
        ci.save
        return ci

    def send_notification(self, event):
        if self.contact_by == ContactInfo.SMS:
            print('TBD: Need to send sms to {}'.format(self.number))
        else:
            # print('sending email to {}'.format(self.email))
            message = '''
Hi,

Monitor "{}" has detected a missed checkin.

The last checkin was at: {:%m/%d %H:%M}

Checkins for this task are supposed to happen every {} hours.

Visit you account: http://watch4.events

Regards,

dane@dacxl.com
watch4.events
'''
            message = message.format(event.sentinel.name, event.time, event.sentinel.freq)
            # print(message)
            subject = 'watch4.events: missed checkin report'
            send_mail(subject, message, 'dane@dacxl.com', [self.email], fail_silently=False)
            Event.add_notification(tag=event.sentinel.tag)

    def __str__(self):
        return '<ContactInfo: {}>'.format(self.user.username)
