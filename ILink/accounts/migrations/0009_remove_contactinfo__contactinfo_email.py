# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 15:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_contactinfo__contactinfo_education'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactinfo',
            name='_contactinfo_email',
        ),
    ]
