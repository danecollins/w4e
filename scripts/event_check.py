#!/Users/dane/env/dj/bin/python
import os
import sys
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from sentinel.models import Sentinel, ContactInfo


def missing_events(debug=False):
    for stn in Sentinel.objects.all():
        status = stn.missed_checkin()
        if status:
            try:
                ci = stn.user.contactinfo
            except:
                ci = ContactInfo.create_default(stn.user)
            ci.send_notification(status)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        missing_events(debug=True)
    else:
        missing_events(debug=False)
