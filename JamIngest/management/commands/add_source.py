from django.core.management.base import BaseCommand

from JamIngest import models


class Command(BaseCommand):
    """Adds a source to BlueJam."""

    help = "Adds a source to BlueJam."

    def add_arguments(self, parser):
        """Adds arguments to Django's management command-line parser.

        :param parser: the parser to which the required arguments will be added
        :return: None
        """
        parser.add_argument('url')
        parser.add_argument('type')
        parser.add_argument('issn')
        parser.add_argument('source name')
        parser.add_argument('target type')

    def handle(self, *args, **options):
        """Imports an OAI feed into Revista.

        :param args: None
        :param options: Dictionary containing 'url', and 'type'
        :return: None
        """
        models.JamSource(url=options['url'], source_type=options['type'], issn=options['issn'],
                         journal_name=options['source name'], target_type=options['target type']).save()
        print("Done.")
