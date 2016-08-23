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
import requests
from bs4 import BeautifulSoup

from JamIngest.importers import shared


# note: URL to pass for import is http://journal.org/journal/oai/


def import_article(journal, url):
    """ Import an Open Journal Systems article.

    :param journal: the journal to import to
    :param url: the URL of the article to import
    :return: None
    """

    # retrieve the remote page and establish if it has a DOI
    already_exists, doi, domain, soup_object = shared.fetch_page_and_check_if_exists(url)

    if already_exists:
        # if here then this article has already been imported
        return

    # fetch basic metadata
    new_article = shared.get_and_set_metadata(journal, soup_object, False, False)

    # get PDF and XML/HTML galleys
    pdf = shared.get_pdf_url(soup_object)

    html = shared.get_soup(soup_object.find('meta', attrs={'name': 'citation_fulltext_html_url'}), 'content')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}
    html = requests.get(html, headers=headers)

    html_contents = BeautifulSoup(html.text, "lxml")
    html_contents = html_contents.find('div', attrs={'id': 'content'})

    if html_contents:
        html_contents = BeautifulSoup(html_contents.decode_contents(formatter=None), "lxml")
        html_contents = html_contents.find('body')
        html_contents = html_contents.decode_contents(formatter=None)

    # attach the galleys to the new article
    galleys = {
        'PDF': pdf,
        'HTML': html_contents
    }

    shared.set_article_galleys_and_identifiers(doi, domain, galleys, new_article, url)

    # save the article to the database
    new_article.save()


def import_oai(journal, soup):
    """ Initiate an OAI import on an Open Journal Systems journal.

    :param journal: the journal to import to
    :param soup: the BeautifulSoup object of the OAI feed
    :return: None
    """
    identifiers = soup.findAll('dc:identifier')

    for identifier in identifiers:
        if identifier.contents[0].startswith('http'):
            print('Parsing {0}'.format(identifier.contents[0]))

            import_article(journal, identifier.contents[0])
