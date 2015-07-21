#!/Users/dane/env/dj/bin/python
import os
import sys
import django
import config.settings
import pytz


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from sentinel.models import Sentinel, Event


def events():
    for stn in Sentinel.objects.all():
        print('\n{}'.format(stn.name))
        for evt in Event.objects.filter(sentinel=stn).order_by('-id')[:2]:
            tm = evt.time
            local = tm.astimezone(pytz.timezone('America/Los_Angeles'))
            print('    {} - {:%m-%d %H:%M}'.format(evt.log_type, local))


if __name__ == '__main__':
    host = config.settings.DATABASES['default']['HOST'] or 'localhost'
    print('\nUsing server: {}'.format(host))
    print('Using database: {}\n'.format(config.settings.DATABASES['default']['NAME']))
    events()
