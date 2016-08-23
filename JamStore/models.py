'''
Copyright (c) Martin Paul Eve 2016

This file is part of BlueJam.

BlueJam is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BlueJam is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BlueJam.  If not, see <http://www.gnu.org/licenses/>.
'''
import os

from django.conf import settings
from django.db import models

from JamStore import files

JAM_TYPES = (
    ('Article', 'Article'),
    ('Book', 'Book'),
    ('Dataset', 'Dataset'),
    ('Image', 'Image'),
    ('Other', 'Other'),
)


class Jam(models.Model):
    jam_type = models.CharField(max_length=10, choices=JAM_TYPES, null=False, blank=False)

    # Metadata
    title = models.CharField(max_length=800)
    abstract = models.TextField()
    license = models.ForeignKey('JamLicense', blank=True, null=True)
    page_numbers = models.CharField(max_length=20, blank=True, null=True)
    authors = models.ManyToManyField('JamAuthor', blank=True, related_name='authors')
    doi = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    issue = models.IntegerField(default=1)
    volume = models.IntegerField(default=1)
    journal = models.ForeignKey('JamJournal')

    # this is a local identifier so that different instances of BlueJam can easily distinguish duplicates
    jam_id = models.CharField(max_length=1000, blank=True, null=True)

    # Files
    files = models.ManyToManyField('JamFile', blank=True, related_name='files')

    # Dates
    date_accepted = models.DateTimeField(auto_now_add=True)
    date_submitted = models.DateTimeField(blank=True, null=True)
    date_published = models.DateTimeField(blank=True, null=True)


class JamLicense(models.Model):
    journal = models.ForeignKey('JamJournal')
    name = models.CharField(max_length=800)
    short_name = models.CharField(max_length=15)
    url = models.URLField(max_length=1000)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return u'%s' % self.short_name


class JamAuthor(models.Model):
    first_name = models.CharField(max_length=300, null=True, blank=True)
    middle_name = models.CharField(max_length=300, null=True, blank=True)
    last_name = models.CharField(max_length=300, null=True, blank=True)
    orcid = models.CharField(max_length=40, null=True, blank=True, verbose_name="ORCiD")

    @property
    def first_names(self):
        return '{0}{1}{2}'.format(self.first_name, ' ' if self.middle_name is not None else '',
                                  self.middle_name if self.middle_name is not None else '')

    @property
    def full_name(self):
        if self.middle_name:
            return u'{0} {1} {2}'.format(self.first_name, self.middle_name, self.last_name)
        else:
            return u'{0} {1}'.format(self.first_name, self.last_name)


class JamJournal(models.Model):
    journal_name = models.CharField(max_length=800, null=True, blank=True)
    journal_issn = models.CharField(max_length=9, null=True, blank=True)


class JamFile(models.Model):
    mime_type = models.CharField(max_length=50)
    original_filename = models.CharField(max_length=1000)
    uuid_filename = models.CharField(max_length=100)
    label = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def get_file(self, article):
        return files.get_file(self, article)

    def get_file_path(self, article):
        return os.path.join(settings.BASE_DIR, 'files', 'articles', str(article.id), str(self.uuid_filename))

    def __str__(self):
        return u'%s' % self.original_filename

    def __repr__(self):
        return u'%s' % self.original_filename
