# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_remove_bares_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bares',
            name='likes',
        ),
    ]
