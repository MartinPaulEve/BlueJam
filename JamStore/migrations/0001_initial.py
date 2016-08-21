# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jam_type', models.CharField(choices=[('Article', 'Article'), ('Book', 'Book'), ('Dataset', 'Dataset'), ('Image', 'Image'), ('Other', 'Other')], max_length=10)),
                ('title', models.CharField(max_length=800)),
                ('abstract', models.TextField()),
                ('page_numbers', models.CharField(blank=True, max_length=20, null=True)),
                ('doi', models.CharField(blank=True, max_length=1000, null=True)),
                ('url', models.CharField(blank=True, max_length=1000, null=True)),
                ('issue', models.IntegerField(default=1)),
                ('volume', models.IntegerField(default=1)),
                ('jam_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('date_accepted', models.DateTimeField(auto_now_add=True)),
                ('date_submitted', models.DateTimeField(blank=True, null=True)),
                ('date_published', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JamAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=300, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=300, null=True)),
                ('last_name', models.CharField(blank=True, max_length=300, null=True)),
                ('orcid', models.CharField(blank=True, max_length=40, null=True, verbose_name='ORCiD')),
            ],
        ),
        migrations.CreateModel(
            name='JamFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mime_type', models.CharField(max_length=50)),
                ('original_filename', models.CharField(max_length=1000)),
                ('uuid_filename', models.CharField(max_length=100)),
                ('label', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JamJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal_name', models.CharField(blank=True, max_length=800, null=True)),
                ('journal_issn', models.CharField(blank=True, max_length=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JamLicense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=800)),
                ('short_name', models.CharField(max_length=15)),
                ('url', models.URLField(max_length=1000)),
                ('text', models.TextField(blank=True, null=True)),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JamStore.JamJournal')),
            ],
        ),
        migrations.AddField(
            model_name='jam',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='authors', to='JamStore.JamAuthor'),
        ),
        migrations.AddField(
            model_name='jam',
            name='files',
            field=models.ManyToManyField(blank=True, related_name='files', to='JamStore.JamFile'),
        ),
        migrations.AddField(
            model_name='jam',
            name='license',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='JamStore.JamLicense'),
        ),
    ]
