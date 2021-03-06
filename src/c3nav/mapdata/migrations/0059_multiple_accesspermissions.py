# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-17 20:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0058_wifimeasurement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accesspermissiontoken',
            name='redeemed_by',
        ),
        migrations.RemoveField(
            model_name='accessrestriction',
            name='users',
        ),
        migrations.AddField(
            model_name='accesspermission',
            name='token',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accesspermissions', to='mapdata.AccessPermissionToken', verbose_name='Access permission token'),
        ),
        migrations.AlterUniqueTogether(
            name='accesspermission',
            unique_together=set([]),
        ),
    ]
