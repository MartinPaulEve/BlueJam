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
