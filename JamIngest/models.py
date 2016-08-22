from django.db import models


class JamSource(models.Model):
    url = models.CharField(max_length=800)
    source_type = models.CharField(max_length=800)
    issn = models.CharField(max_length=9)
    source_name = models.CharField(max_length=800)
    target_type = models.CharField(max_length=300)
