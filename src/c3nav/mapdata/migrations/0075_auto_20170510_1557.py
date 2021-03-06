# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-10 15:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0074_auto_20170510_1556'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='slug_ptr',
            new_name='locationslug_ptr',
        ),
        migrations.RenameField(
            model_name='locationgroup',
            old_name='slug_ptr',
            new_name='locationslug_ptr',
        ),
        migrations.RenameField(
            model_name='point',
            old_name='slug_ptr',
            new_name='locationslug_ptr',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='slug_ptr',
            new_name='locationslug_ptr',
        ),
        migrations.RenameField(
            model_name='space',
            old_name='slug_ptr',
            new_name='locationslug_ptr',
        ),
    ]
