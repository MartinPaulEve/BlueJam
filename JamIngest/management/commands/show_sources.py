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
            print('[{0}] \'{1}\' {2}, {3}, {4}, {5}'.format(source.id, source.target_type, source.source_name,
                                                          source.issn, source.source_type, source.url))

        print("Done.")
