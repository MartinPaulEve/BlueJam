from django.core.management.base import BaseCommand

from JamIngest import importer, models


class Command(BaseCommand):
    """Pulls OAI PMH feeds into BlueJam."""

    help = "Pulls OAI PMH feeds into BlueJam."

    def handle(self, *args, **options):
        """Imports an OAI feed into Revista.

        :param args: None
        :param options: Dictionary containing 'url', 'journal_id', 'user_id', and a boolean '--delete' flag
        :return: None
        """

        jams = models.JamSource.objects.filter(source_type='OAI')

        for jam in jams:

            jam_dict = {'url': jam.url,
                        'issn': jam.issn}

            importer.import_oai(**jam_dict)
