from django.core.management.base import BaseCommand

from JamIngest import importer


class Command(BaseCommand):
    """Pulls a remote BlueJam feed into this BlueJam instance."""

    help = "Pulls a remote BlueJam feed into this BlueJam instance."

    def handle(self, *args, **options):
        """Imports an OAI feed into Revista.

        :param args: None
        :param options: Dictionary containing 'url', 'journal_id', 'user_id', and a boolean '--delete' flag
        :return: None
        """
        importer.import_bluejam(**options)
