# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-22 16:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JamStore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jam',
            name='journal',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='JamStore.JamJournal'),
            preserve_default=False,
        ),
    ]
