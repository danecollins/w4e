#!/Users/dane/env/dj/bin/python
import os
import sys
import django
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail

import requests
import datetime
import pytz
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from sentinel.models import Sentinel, Event, ContactInfo

# everything in UTC since that is what is in the database
utc = pytz.UTC


def missing_events(debug=False):
    grace_period = 2  # minutes
    sentinels = Sentinel.objects.all()
    now = timezone.now()

    for stn in sentinels:
        if stn.active:
            delta = datetime.timedelta(hours=stn.freq, minutes=grace_period)
            expected = now - delta
            last_event = Event.objects.filter(tag=stn.tag).order_by('-id')
            if last_event:
                last_event = last_event[0]
            else:
                # this tag has never checked in so skip it
                if debug:
                    print('{} has never checked in'.format(stn.name))
                continue

            # if there has never been a checkin or notification already sent, skip
            if last_event and last_event.log_type == Event.LOG:
                last_time = last_event.time
                if last_time < expected:
                    # get last event time
                    last_seen = str(last_time)
                    last_seen = last_seen.split(".")[0]
                    msg = 'Monitor "{}". Last seen: {:%m/%d %H:%M}, Current={:%m/%d %H:%M}'
                    msg = msg.format(stn.name, last_seen, now)
                    print(msg)

                    # when an event is missed we want to add a notification in the event queue.
                    # we will not send a notification out if the last event in the queue is a
                    # notification event.
                    Event.add_notification(stn.tag)

                    ci = ContactInfo.objects.get(user=stn.user)
                    if ci.contact_by == ContactInfo.SMS:
                        print('TBD: Need to send sms to {}'.format(ci.number))
                    else:
                        print('sending email to {}'.format(ci.email))
                        send_mail('watch4.events: event missed', msg, 'dane@dacxl.com',
                                  [ci.email], fail_silently=False)
                else:
                    if debug:
                        print('Last "{}"'.format(stn.name))
                        print('    expected: {:%m/%d %H:%M}'.format(expected))
                        print('    occurred: {:%m/%d %H:%M}'.format(last_time))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        missing_events(debug=True)
    else:
        missing_events(debug=False)
