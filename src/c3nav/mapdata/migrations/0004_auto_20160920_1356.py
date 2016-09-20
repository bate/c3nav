# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 13:56
from __future__ import unicode_literals

import c3nav.mapdata.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0003_package_commit_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='type',
        ),
        migrations.AddField(
            model_name='feature',
            name='feature_type',
            field=models.CharField(choices=[('building', 'Building'), ('room', 'Room'), ('outside', 'Outside Area'), ('obstacle', 'Obstacle')], default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feature',
            name='geometry',
            field=c3nav.mapdata.fields.GeometryField(),
        ),
    ]
