from django.core.management.base import BaseCommand

from JamIngest import models


class Command(BaseCommand):
    """Deletes a source from BlueJam."""

    help = "Deletes a source from BlueJam."

    def add_arguments(self, parser):
        """Adds arguments to Django's management command-line parser.

        :param parser: the parser to which the required arguments will be added
        :return: None
        """
        parser.add_argument('id')

    def handle(self, *args, **options):
        """Imports an OAI feed into Revista.

        :param args: None
        :param options: Dictionary containing 'url', and 'type'
        :return: None
        """
        models.JamSource.objects.get(pk=options['id']).delete()
        print("Done.")
