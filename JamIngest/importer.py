from JamStore import models

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from JamIngest.importers import up, ojs


def identify_journal_type_by_oai(url):
    """ Attempts to identify the type of journal we are dealing with based on the OAI URL.

    :param url: the URL to the OAI feed
    :return: a string containing the type of journal
    """
    if u'/jms/index.php/up/oai/' in url:
        return "UP"

    if (u'?journal=' in url and u'?page=oai') or '/oai' in url:
        return "OJS"


def import_ojs_article(**options):
    """ Imports a single article from an Open Journal Systems installation

    :param options: a dictionary containing 'journal_id', 'user_id', 'url' and optionally a 'delete' flag
    :return: None
    """
    journal = models.JamJournal.objects.get(pk=options['journal_id'])
    url = options['url']

    ojs.import_article(journal, url)


def import_up_article(**options):
    """ Imports a single article from a Ubiquity Press installation

    :param options: a dictionary containing 'journal_id', 'user_id', 'url' and optionally a 'delete' flag
    :return: None
    """
    journal = models.JamJournal.objects.get(pk=options['journal_id'])
    url = options['url']

    up.import_article(journal, url)


def import_oai(**options):
    """ Imports an OAI feed

    :param options: a dictionary containing 'journal_id', 'user_id', 'url' and optionally a 'delete' flag
    :return: None
    """
    journal = models.JamJournal.objects.get(pk=options['journal_id'])

    verb = '?verb=ListRecords&metadataPrefix=oai_dc'
    url = options['url'] + verb

    journal_type = identify_journal_type_by_oai(url)

    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    if journal_type == "UP":
        print("Detected journal type as UP. Processing.")
        up.import_oai(journal, soup, domain)
    elif journal_type == "OJS":
        print("Detected journal type as OJS. Processing.")
        ojs.import_oai(journal, soup)
    else:
        print("Journal type currently unsupported")
