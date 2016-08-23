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
                         source_name=options['source name'], target_type=options['target type']).save()
        print("Done.")
