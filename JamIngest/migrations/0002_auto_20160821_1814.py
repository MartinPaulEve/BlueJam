# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JamIngest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jamsource',
            name='issn',
            field=models.CharField(default=0, max_length=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jamsource',
            name='journal_name',
            field=models.CharField(default='OLHJ', max_length=800),
            preserve_default=False,
        ),
    ]