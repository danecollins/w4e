# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentinel', '0005_auto_20150714_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sentinel',
            field=models.ForeignKey(default=1, to='sentinel.Sentinel'),
            preserve_default=False,
        ),
    ]
