# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-27 16:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0005_auto_20170527_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='name',
        ),
    ]