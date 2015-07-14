# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentinel', '0004_auto_20150714_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='number',
            field=models.CharField(max_length=16, blank=True),
        ),
    ]
