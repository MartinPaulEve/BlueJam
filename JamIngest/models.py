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
from django.db import models


class JamSource(models.Model):
    url = models.CharField(max_length=800)
    source_type = models.CharField(max_length=800)
    issn = models.CharField(max_length=9)
    source_name = models.CharField(max_length=800)
    target_type = models.CharField(max_length=300)
