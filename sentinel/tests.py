from __future__ import print_function
from __future__ import unicode_literals
import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User

from sentinel.models import Event, Sentinel, ContactInfo
from django.utils import timezone


def username(n):
    return 'test{}'.format(n)


def get_user(n):
    return User.objects.get(username=username(n))


def create_users():
    u = User.objects.create_user(username=username(1), password='password',
                                 email="{}@watch4.events".format(username(1)))
    u.save()
    u = User.objects.create_user(username=username(2), password='password')
    u.save()


def get_tag():
    return '12345'


def create_sentinel(u):
    s = Sentinel(user=u, tag=get_tag(), name='monitor1', freq=1)
    s.save()
    return s


#############################################################################
#
# Model Tests
#
class TestContactInfoModel(TestCase):
    def test_simple_create_default(self):
        create_users()
        u = get_user(1)
        ci = ContactInfo.create_default(u)
        self.assertEqual(ci.email, 'test1@watch4.events')
        self.assertEqual(ci.contact_by, ContactInfo.EMAIL)


class TestSentinelModel(TestCase):
    def test_simple_create(self):
        create_users()
        u = get_user(1)
        create_sentinel(u)
        self.assertEqual(Sentinel.objects.count(), 1)

    def test_missed_checkin(self):
        create_users()
        u = get_user(1)
        s = create_sentinel(u)
        now = timezone.now()
        future_time = now + datetime.timedelta(hours=2)
        Event.add_checkin(tag=get_tag())
        status = s.missed_checkin(test=future_time)
        self.assertTrue(status)
        future_time = now + datetime.timedelta(minutes=55)
        status = s.missed_checkin(test=future_time)
        self.assertFalse(status)


class TestEventModel(TestCase):
    def test_simple_create(self):
        create_users()
        u = get_user(1)
        create_sentinel(u)
        Event.add_checkin(get_tag())
        self.assertEqual(Event.objects.count(), 1)

    def test_recent(self):
        create_users()
        u = get_user(1)
        create_sentinel(u)
        for i in range(40):
            Event.add_checkin(get_tag())
        l = Event.recent()
        self.assertEqual(len(l), 30)


#############################################################################
#
# View Tests
#
class TestViewHome(TestCase):
    def test_check_links(self):
        c = Client()
        text = c.get('/').content
        self.assertTrue(text.find('Sign In') != -1)
        self.assertTrue(text.find('Sign Up') != -1)
