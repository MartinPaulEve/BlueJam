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
from django.core.management.base import BaseCommand

from JamIngest import importer, models
from JamStore import models as JamModels


class Command(BaseCommand):
    """Pulls OAI PMH feeds into BlueJam."""

    help = "Pulls OAI PMH feeds into BlueJam."

    def handle(self, *args, **options):
        """Imports an OAI feed into Revista.

        :param args: None
        :param options: None
        :return: None
        """

        jam_sources = models.JamSource.objects.filter(source_type='OAI')

        for jam_source in jam_sources:

            if jam_source.target_type == 'journal':
                journal, created = JamModels.JamJournal.objects.get_or_create(journal_issn=jam_source.issn,
                                                                                journal_name=jam_source.source_name)

                if created:
                    print('Created new JamJournal container: \'{0}\''.format(jam_source.source_name))

            jam_dict = {'url': jam_source.url,
                        'journal': journal,
                        'jam_source': jam_source}

            importer.import_oai(**jam_dict)
