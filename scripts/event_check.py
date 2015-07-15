#!/Users/dane/env/dj/bin/python
import os
import sys
import django
from django.conf import settings
from django.utils import timezone
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
    sentinels = Sentinel.objects.all()
    now = timezone.now()

    for w in sentinels:
        if w.active:
            delta = datetime.timedelta(hours=w.freq)
            expected = now - delta
            last_event = Event.objects.filter(tag=w.tag).order_by('-id')[0]

            # if there has never been a checkin or notification already sent, skip
            if last_event and last_event.log_type == Event.LOG:
                last_time = last_event.time
                if last_time < expected:
                    # get last event time
                    last_seen = str(last_time)
                    last_seen = l.split(".")[0]
                    msg = 'Missed event for monitor "{}". Last seen: {}'.format(w.name, last_seen)
                    print(msg)

                    # when an event is missed we want to add a notification in the event queue.
                    # we will not send a notification out if the last event in the queue is a
                    # notification event.
                    ev = Event(time=now, tag=w.tag, log_type=Event.NOT)
                    ev.save()

                    ci = ContactInfo.objects.get(user=w.user)
                    if ci.contact_type == ContactInfo.SMS:
                        print('TBD: Need to send sms to {}'.format(ci.number))
                    else:
                        print('TBD: Need to send email to {}'.format(ci.email))
                else:
                    if debug:
                        print('Last "{}"'.format(w.name))
                        print('    expected: {}'.format(expected))
                        print('    occurred: {}'.format(last_time))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        missing_events(debug=True)
    else:
        missing_events(debug=False)
