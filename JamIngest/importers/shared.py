import codecs
import os
from datetime import datetime
from urllib.parse import urlparse
from uuid import uuid4

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone

from JamStore import models


def fetch_images_and_rewrite_xml_paths(base, root, contents, article):
    """Download images from an XML or HTML document and rewrite the new galley to point to the correct source.

    :param base: a base URL for the remote journal install e.g. http://www.myjournal.org
    :param root: the root page (i.e. the article that we are grabbing from) e.g. /article/view/27
    :param contents: the current page's HTML or XML
    :param article: the new article to which this download should be attributed
    :return: a string of the rewritten XML or HTML
    """

    # create a BeautifulSoup instance of the page's HTML or XML
    soup = BeautifulSoup(contents, 'lxml')

    # add element:attribute properties here for images that should be downloaded and have their paths rewritten
    # so 'img':'src' means look for elements called 'img' with an attribute 'src'
    elements = {
        'img': 'src',
        'graphic': 'xlink:href'
    }

    # iterate over all found elements
    for element, attribute in elements. items():
        images = soup.findAll(element)

        # iterate over all found elements of each type in the elements dictionary
        for idx, val in enumerate(images):

            # attempt to pull a URL from the specified attribute
            url = get_soup(val, attribute)

            if url:
                url_to_use = url

                # this is a Ubiquity Press-specific fix to rewrite the path so that we don't hit OJS's dud backend
                if not url.startswith('/') and not url.startswith('http'):
                    url_to_use = root.replace('/article/view', '/articles') + '/' + url

                # download the image file
                filename, mime = fetch_file(base, url_to_use, root, '', article, handle_images=False)

                # determine the MIME type and slice the first open bracket and everything after the comma off
                mime = mime.split(',')[0][1:].replace("'", "")

                # store this image in the database affiliated with the new article
                new_file = add_file(mime, '', 'Galley image', filename, article, False)
                absolute_new_filename = reverse('article_file_download',
                                                kwargs={'identifier': article.id, 'file_id': new_file.id})

                # rewrite the HTML or XML contents to point to the new image filename (a reverse lookup of
                # article_file_download)
                print('Replacing image URL {0} with {1}'.format(url, absolute_new_filename))
                contents = str(contents).replace(url, absolute_new_filename)

    return contents


def parse_date(date_string, is_iso):
    """ Parse a date from a string according to timezone-specific settings

    :param date_string: the date string to be parsed
    :param is_iso: whether or not to use ISO-specific formatting settings ("%Y-%m-%dT%H:%M:%S" if True, otherwise
    "%Y-%m-%d"
    :return: a timezone object of the parsed date
    """
    if date_string is not None and date_string != "":
        if is_iso:
            return timezone.make_aware(datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S"),
                                       timezone.get_current_timezone())
        else:
            return timezone.make_aware(datetime.strptime(date_string, "%Y-%m-%d"), timezone.get_current_timezone())
    else:
        print("Returning current datetime as no valid datetime was given")
        return timezone.now()


def fetch_file(base, url, root, extension, article, handle_images=False):
    """ Download a remote file and store in the database affiliated to a specific article

    :param base: a base URL for the remote journal install e.g. http://www.myjournal.org
    :param url: either a full URL or a suffix to base that when concatenated will form a whole URL to the image
    :param root: either a full URL or a suffix to base that when concatenated will form a whole URL to the XML/HTML
    :param extension: the file extension of the file that we will download
    :param article: the new article to which this download should be attributed
    :param handle_images: whether or not to extract, download and parse images within the downloaded file
    :return: a tuple of the filename and MIME-type
    """

    # if this is not a full URL concatenate base and URL to form the full address
    if not url.startswith('http'):
        url = base + url

    print('Fetching {0}'.format(url))

    # imitate headers from a browser to avoid being blocked on some installs
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}

    # send the request to the remote server
    req = requests.get(url, headers=headers, stream=True)

    # set the filename to a unique UUID4 identifier with the passed file extension
    filename = '{0}.{1}'.format(uuid4(), extension)

    # set the path to save to be the sub-directory for the article
    path = os.path.join(settings.BASE_DIR, 'files', 'articles', str(article.id))

    # create the sub-folders as necessary
    if not os.path.exists(path):
        os.makedirs(path, 0o0775)

    # save the downloaded file to the article's sub-folder with the correct encoding
    resp = bytes()

    with codecs.open(os.path.join(path, filename), 'wb') as f:
        for chunk in req.iter_content(chunk_size=512 * 1024, decode_unicode=True):
            resp += chunk

        # intercept the request if we need to parse this as HTML or XML with images to rewrite
        if handle_images:
            resp = fetch_images_and_rewrite_xml_paths(base, root, resp, article)

        if type(resp) is str:
            resp = bytes(resp)

        f.write(resp)

    # return the filename and MIME type
    return filename, req.headers.get('content-type')


def save_file(base, contents, root, extension, article, handle_images=False):
    """ Save 'contents' to disk as a file associated with 'article'

    :param base: a base URL for the remote journal install e.g. http://www.myjournal.org
    :param contents: the contents to be written to disk
    :param root: either a full URL or a suffix to base that when concatenated will form a whole URL to the XML/HTML
    :param extension: the file extension of the file that we will download
    :param article: the new article to which this download should be attributed
    :param handle_images: whether or not to extract, download and parse images within the downloaded file
    :return: the filename of the written file
    """

    # assign a unique UUID4 to be the filename
    filename = '{0}.{1}'.format(uuid4(), extension)

    # set the path to the article's sub-folder
    path = os.path.join(settings.BASE_DIR, 'files', 'articles', str(article.id))

    # decode the contents to UTF-16
    contents = contents

    # create the sub-folder structure if needed
    if not os.path.exists(path):
        os.makedirs(path, 0o0775)

    # write the file to disk
    with codecs.open(os.path.join(path, filename), 'wb') as f:
        # process any images if instructed
        if handle_images:
            contents = fetch_images_and_rewrite_xml_paths(base, root, contents, article)

        f.write(contents)

    return filename


def add_file(file_mime, extension, description, filename, article, galley=True, thumbnail=False):
    """ Add a file to the File model in core. Saves a file to the database affiliated with an article.

    :param file_mime: the MIME type of the file. Used in serving the file back to users
    :param extension: the extension of the file
    :param description: a description of the file
    :param filename: the filename
    :param article: the article with which the file is associated
    :param galley: whether or not this is a galley file
    :param thumbnail: whether or not this is a thumbnail
    :return: the new File object
    """

    # create a new File object with the passed parameters
    new_file = models.JamFile(
        mime_type=file_mime,
        original_filename='file.{0}'.format(extension),
        uuid_filename=filename,
        label=extension.upper(),
        description=description,
    )

    if thumbnail:
        article.thumbnail_image_file = new_file
        article.save()
        return new_file

    new_file.save()
    article.save()

    return new_file


def get_soup(soup_object, field_name, default=None):
    """ Parses a soup object and returns field_name if found, otherwise default

    :param soup_object: the BeautifulSoup object to parse
    :param field_name: the name of the field to look for
    :param default: the default to return if it isn't found
    :return: a default value to return if the soup_object is None
    """
    if soup_object:
        return soup_object.get(field_name, None)
    else:
        return default


def parse_url(url):
    """ Parses a URL into a well-formed and navigable format

    :param url: the URL to parse
    :return: the formatted URL
    """
    return '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))


def fetch_page(url):
    """ Fetches a remote page and returns a BeautifulSoup object

    :param url: the URL to fetch
    :return: a BeautifulSoup object
    """
    return BeautifulSoup(requests.get(url).text, 'lxml')


def extract_and_check_doi(soup_object):
    """
    Extracts a DOI from a soup_object of a page and returns a Tuple of the DOI and whether we already have it in the
    local journal.

    :param soup_object: a BeautifulSoup object of a page
    :return: a tuple of the doi and whether it exists locally (a boolean)
    """
    # see whether there's a DOI and, most importantly, whether it's a duplicate
    doi = get_soup(soup_object.find('meta', attrs={'name': 'citation_doi'}), 'content')

    if doi:
        identifier = models.Jam.objects.filter(doi=doi)

        if identifier:
            print('DOI {0} already imported. Skipping.'.format(doi))
            return doi, True
        else:
            return doi, False
    else:
        return doi, False


def get_author_info(soup_object):
    """ Extract authors, emails, and institutional affiliation from a BeautifulSoup object.

    :param soup_object: a BeautifulSoup object of a page
    :return: a tuple of authors, emails, institutions and a boolean of whether we have emails for all authors
    """
    authors = soup_object.findAll('meta', attrs={'name': 'citation_author'})
    emails = soup_object.findAll('meta', attrs={'name': 'citation_author_email'})
    institutions = soup_object.findAll('meta', attrs={'name': 'citation_author_institution'})

    mismatch = len(authors) != len(emails)

    if mismatch:
        print('Mismatch in number of authors, emails and institutions added. This article will not be '
              'correctly attributed.')

    return authors, emails, institutions, mismatch


def get_pdf_url(soup_object):
    """
    Returns the value of the meta tag where the name attribute is citation_pdf_url from a BeautifulSoup object of a
    page.

    :param soup_object: a BeautifulSoup object of a page
    :return: a string of the PDF URL
    """
    return get_soup(soup_object.find('meta', attrs={'name': 'citation_pdf_url'}), 'content')


def get_dates(soup_object, date_published_iso=False, date_submitted_iso=False):
    """ Extracts publication dates from a BeautifulSoup object of a page.

    :param soup_object: a BeautifulSoup object of a page
    :param date_published_iso: whether or not the date_published is in an ISO date format
    :param date_submitted_iso: whether or not the date_submitted is in an ISO date format
    :return: a tuple of the date published and the date submitted
    """
    date_published = parse_date(
        get_soup(soup_object.find('meta', attrs={'name': 'citation_publication_date'}), 'content'), date_published_iso)

    date_submitted = parse_date(get_soup(soup_object.find('meta', attrs={'name': 'DC.Date.dateSubmitted'}), 'content'),
                                date_submitted_iso)

    return date_published, date_submitted


def create_new_article(date_published, date_submitted, journal, soup_object):
    """ Create a new article in the database.

    :param date_published: the date the article was published
    :param date_submitted: the date the article was submitted
    :param journal: the journal to which the article belongs
    :param soup_object: the BeautifulSoup object from which to extract the remaining fields
    :return: a tuple of a dictionary information about the article and the new article object
    """

    article_dict = {
        'title': get_soup(soup_object.find('meta', attrs={'name': 'DC.Title'}), 'content'),
        'abstract': get_soup(soup_object.find('meta', attrs={'name': 'DC.Description'}), 'content', ''),
        'date_published': date_published,
        'date_submitted': date_submitted,
        'journal': journal,
        'page_numbers': get_soup(soup_object.find('meta', attrs={'name': 'DC.Identifier.pageNumber'}), 'content', '')
    }

    new_article = models.Jam.objects.create(**article_dict)

    return article_dict, new_article


def set_article_attributions(authors, article):
    """ Set author, email, and institution information on an article

    :param authors: the authors of the article
    :param article: the article on which this attribution information should be set
    :return: None
    """

    for idx, val in enumerate(authors):
        author_name = get_soup(val, 'content')

        # add an account for this new user
        account = models.JamAuthor.objects.filter(first_name=' '.join(author_name.split(' ')[:-1]),
                                                  last_name=author_name.split(' ')[-1])

        if account is not None and len(account) > 0:
            account = account[0]
            print("Found account for {0}".format(author_name))
        else:
            print("Didn't find account for {0}. Creating.".format(author_name))
            account = models.JamAuthor.objects.create(first_name=' '.join(author_name.split(' ')[:-1]),
                                                      last_name=author_name.split(' ')[-1])
            account.save()

        if account:
            article.authors.add(account)


def set_article_issue_and_volume(article, soup_object):
    """ Set the article's issue and volume

    :param article: the article in question
    :param soup_object: a BeautifulSoup object of a page
    :return: None
    """
    issue = int(get_soup(soup_object.find('meta', attrs={'name': 'citation_issue'}), 'content', 0))
    volume = int(get_soup(soup_object.find('meta', attrs={'name': 'citation_volume'}), 'content', 0))

    if issue == 0:
        issue = int(get_soup(soup_object.find('meta', attrs={'name': 'DC.Source.Issue'}), 'content', 0))
    if volume == 0:
        volume = int(get_soup(soup_object.find('meta', attrs={'name': 'DC.Source.Volume'}), 'content', 0))

    article.issue = issue
    article.volume = volume


def set_article_galleys(domain, galleys, article, url):
    """ Attach a set of remote galley files to the local article

    :param domain: the formatted domain object for the remote file
    :param galleys: a dictionary of named galley URLs to harvest
    :param article: the article to which to attach the galleys
    :param url: the URL of the remote galley
    :return: None
    """
    for galley_name, galley in galleys.items():
        if galley:
            if galley_name == 'PDF' or galley_name == 'XML':
                handle_images = True if galley_name == 'XML' else False
                filename, mime = fetch_file(domain, galley, url, galley_name.lower(), article,
                                            handle_images=handle_images)
                add_file('application/{0}'.format(galley_name.lower()), galley_name.lower(),
                         'Galley {0}'.format(galley_name), filename, article)
            else:
                # assuming that this is HTML, which we save to disk rather than fetching
                handle_images = True if galley_name == 'HTML' else False
                filename = save_file(domain, galley, url, galley_name.lower(), article,
                                     handle_images=handle_images)
                add_file('text/{0}'.format(galley_name.lower()), galley_name.lower(),
                         'Galley {0}'.format(galley_name), filename, article)


def set_article_identifier(doi, article):
    """ Save an identifier to the article

    :param doi: the DOI to save
    :param article: the article on which to act
    :return: None
    """
    if doi:
        article.doi = doi
        print("Article imported with ID: {0}".format(doi))
    else:
        print("Article imported with ID: {0}".format(article.id))


def fetch_page_and_check_if_exists(url):
    """ Fetch a remote URL and check if the DOI already exists

    :param url: the URL of the remote page
    :return: tuple of whether the DOI already exists locally, the DOI, the formatted domain, and the BeautifulSoup
    object of the page
    """

    domain = parse_url(url)
    soup_object = fetch_page(url)
    doi, already_exists = extract_and_check_doi(soup_object)

    return already_exists, doi, domain, soup_object


def get_and_set_metadata(journal, soup_object, date_published_iso, date_submitted_iso):
    """ Fetch article metadata and attach it to the article

    :param journal: the journal to which the article should belong
    :param soup_object: a BeautifulSoup object of the page
    :param date_published_iso: whether or not the date published field is in ISO date format
    :param date_submitted_iso: date_published_iso: whether or not the date submitted field is in ISO date format
    :return: the new article
    """
    authors, emails, institutions, mismatch = get_author_info(soup_object)

    date_published, date_submitted = get_dates(soup_object, date_published_iso=date_published_iso,
                                               date_submitted_iso=date_submitted_iso)

    article_dict, new_article = create_new_article(date_published, date_submitted, journal, soup_object)

    set_article_attributions(authors, new_article)
    set_article_issue_and_volume(new_article, soup_object)

    return new_article


def set_article_galleys_and_identifiers(doi, domain, galleys, article, url):
    """ Set the galleys and identifiers on an article

    :param doi: the DOI
    :param domain: the formatted URL domain string
    :param galleys: the galleys dictionary to parse
    :param article: the article in question
    :param url: the URL of the remote galley
    :return: None
    """
    set_article_galleys(domain, galleys, article, url)
    set_article_identifier(doi, article)
