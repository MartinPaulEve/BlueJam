from django.core.management.base import BaseCommand

from JamIngest import models


class Command(BaseCommand):
    """Show sources in BlueJam."""

    help = "Show sources in BlueJam."

    def handle(self, *args, **options):
        """Imports an OAI feed into Revista.

        :param args: None
        :param options: Dictionary containing 'url', and 'type'
        :return: None
        """
        sources = models.JamSource.objects.all()

        for source in sources:
            print('[{0}]: {1}, {2}, {3}, {4}'.format(source.id, source.source_name, source.issn, source.source_type,
                                                     source.url))

        print("Done.")
