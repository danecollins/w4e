from django.db import models

import string
import random
import pytz

pst = pytz.timezone('America/Los_Angeles')


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Event(models.Model):
    LOG = 'LOG'
    NOTIFICATION = 'NOT'
    TYPE_CHOICES = (
        (LOG, 'Log'),
        (NOTIFICATION, 'Notification')
    )
    time = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=30)
    log_type = models.CharField(max_length=3,
                                choices=TYPE_CHOICES,
                                default=LOG)

    @classmethod
    def recent(self):
        events = Event.objects.all().order_by('-id')[:30]
        tags = set([x.tag for x in events])
        tag_name = {tag: Sentinel.objects.get(tag=tag).name for tag in tags}
        event_list = []
        for e in events:
            e.name = tag_name[e.tag]
            event_list.append(e)
        return event_list

    def __str__(self):
        tm = self.time.astimezone(pst)
        time_str = tm.strftime('%h-%d %H:%M')
        return 'Event({},{},{})'.format(self.tag,
                                        time_str,
                                        self.log_type)

    def __repr__(self):
        return 'Event({},{},{}'.format(self.tag, self.time, self.log_type)


class Sentinel(models.Model):
    name = models.CharField(max_length=40)
    tag = models.CharField(max_length=8)
    freq = models.IntegerField()
    active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return 'Sentinel({},{},{},{})'.format(self.name,
                                             self.tag,
                                             self.freq,
                                             self.active)

    def __repr__(self):
        return "Sentinel(name='{}', tag='{}', freq={}, active={})".format(self.name,
                                                                         self.tag,
                                                                         self.freq,
                                                                         self.active)
