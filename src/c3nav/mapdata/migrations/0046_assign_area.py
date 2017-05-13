# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-04 13:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def assign_area(apps, schema_editor):
    Level = apps.get_model('mapdata', 'Level')
    for level in Level.objects.all():
        level_areas = list(level.areas.all())
        for c in ('escalators', 'obstacles', 'lineobstacles', 'stairs', 'stuffedareas'):
            getattr(level, c).filter(name__endswith='_').delete()
            for obj in getattr(level, c).all():
                geom = obj.buffered_geometry if hasattr(obj, 'buffered_geometry') else obj.geometry
                areas = [a for a in level_areas if a.geometry.intersects(geom)]
                if not areas:
                    obj.delete()
                    continue
                for area in areas:
                    obj.area = area
                    obj.save()
                    obj.pk = None
                    obj.name += '_'


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0045_merge_areas'),
    ]

    operations = [
        migrations.AddField(
            model_name='escalator',
            name='area',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='escalators', to='mapdata.Area', verbose_name='area'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lineobstacle',
            name='area',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='lineobstacles', to='mapdata.Area', verbose_name='area'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='obstacle',
            name='area',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='obstacles', to='mapdata.Area', verbose_name='area'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stair',
            name='area',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='stairs', to='mapdata.Area', verbose_name='area'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stuffedarea',
            name='area',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='stuffedareas', to='mapdata.Area', verbose_name='area'),
            preserve_default=False,
        ),
        migrations.RunPython(assign_area),
    ]