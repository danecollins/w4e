# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sentinel', '0002_auto_20150708_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_by', models.CharField(default=b'EMAIL', max_length=5, choices=[(b'SMS', b'SMS'),
                                                                                         (b'EMAIL', b'Email')])),
                ('email', models.CharField(max_length=40, blank=True)),
                ('number', models.CharField(max_length=12, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
