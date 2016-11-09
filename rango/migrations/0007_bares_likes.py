# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_tapas_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='bares',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
