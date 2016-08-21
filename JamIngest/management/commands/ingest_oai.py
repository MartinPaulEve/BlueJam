from django.core.management.base import BaseCommand

from JamIngest import importer


class Command(BaseCommand):
    """Pulls OAI PMH feeds into BlueJam."""

    help = "Pulls OAI PMH feeds into BlueJam."

    def handle(self, *args, **options):
        """Imports an OAI feed into Revista.

        :param args: None
        :param options: Dictionary containing 'url', 'journal_id', 'user_id', and a boolean '--delete' flag
        :return: None
        """
        importer.import_oai(**options)
