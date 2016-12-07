# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0007_bares_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tapas',
            name='url',
        ),
    ]
