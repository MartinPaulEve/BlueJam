import re

import requests
from bs4 import BeautifulSoup

from JamIngest.importers import shared


# note: URL to pass for import is http://journal.org/jms/index.php/up/oai/


def import_article(journal, url):
    """ Import a Ubiquity Press article.

    :param journal: the journal to import to
    :param url: the URL of the article to import
    :param thumb_path: the base path for thumbnails
    :return: None
    """

    # retrieve the remote page and establish if it has a DOI
    already_exists, doi, domain, soup_object = shared.fetch_page_and_check_if_exists(url)

    if already_exists:
        # if here then this article has already been imported
        return

    # fetch basic metadata
    new_article = shared.get_and_set_metadata(journal, soup_object, False, True)

    # get PDF and XML galleys
    pdf = shared.get_pdf_url(soup_object)

    # identify the XML galley using a simple regular expression
    pattern = re.compile('^XML$')
    xml = soup_object.find('a', text=pattern)
    html = None

    if xml:
        xml = xml.get('href', None)
    else:
        # looks like there isn't any XML
        # instead we'll pull out any div with an id of "xml-article" and add as an HTML galley
        html = soup_object.find('div', attrs={'id': 'xml-article'})

        if html:
            html = str(html.contents[0])

    # attach the galleys to the new article
    galleys = {
        'PDF': pdf,
        'XML': xml,
        'HTML': html
    }

    shared.set_article_galleys_and_identifiers(doi, domain, galleys, new_article, url)

    # save the article to the database
    new_article.save()


def import_oai(journal, soup, domain):
    """ Initiate an OAI import on a Ubiquity Press journal.

    :param journal: the journal to import to
    :param soup: the BeautifulSoup object of the OAI feed
    :param domain: the domain of the journal (for extracing thumbnails)
    :return: None
    """

    identifiers = soup.findAll('dc:identifier')

    for identifier in identifiers:
        # rewrite the phrase /jms in Ubiquity Press OAI feeds to get version with
        # full and proper email metadata
        identifier.contents[0] = identifier.contents[0].replace('/jms', '')
        if identifier.contents[0].startswith('http'):
            print('Parsing {0}'.format(identifier.contents[0]))

            import_article(journal, identifier.contents[0])
