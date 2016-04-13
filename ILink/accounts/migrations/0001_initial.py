# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_account_name', models.CharField(max_length=30, unique=True)),
                ('_account_passwd', models.CharField(max_length=50)),
                ('_account_register_date', models.DateField()),
            ],
        ),
    ]