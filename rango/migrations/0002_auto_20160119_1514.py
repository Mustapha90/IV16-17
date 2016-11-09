# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bares',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bares',
            name='slug',
            field=models.SlugField(default=datetime.date(2016, 1, 19)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bares',
            name='views',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
