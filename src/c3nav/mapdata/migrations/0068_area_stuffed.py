# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-10 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0067_auto_20170510_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='stuffed',
            field=models.BooleanField(default=True, verbose_name='stuffed area'),
            preserve_default=False,
        ),
    ]
