# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-19 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20160518_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_expire_date',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_start_date',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
