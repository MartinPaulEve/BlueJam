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
import mimetypes as mime
import os
from uuid import uuid4
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import StreamingHttpResponse

from JamStore import models


def get_file(file_to_get, article):
    """Returns the content of a file using standard python open procedures (no encoding).

    :param file_to_get: the file object to retrieve
    :param article: the associated article
    :return: the contents of the file
    """
    path = os.path.join(settings.BASE_DIR, 'files', 'articles', str(article.id), str(file_to_get.uuid_filename))

    if not os.path.isfile(path):
        return ""

    with open(path, 'r') as content_file:
        content = content_file.read()
        return content


def guess_mime(filename):
    """ Attempt to ascertain the MIME type of a file

    :param filename: the filename of which to guess the type
    :return: the MIME type
    """
    file_mime = mime.guess_type(filename)

    try:
        file_mime = file_mime[0]
    except IndexError:
        file_mime = 'unknown'
    if not file_mime:
        file_mime = 'unknown'

    return file_mime


def serve_file_to_browser(file_path, file_to_serve):
    """ Stream a file to the browser in a safe way

    :param file_path: the path on disk to the file
    :param file_to_serve: the core.models.File object to serve
    :return: HttpStreamingResponse object
    """
    # stream the response to the browser
    # we use the UUID filename to avoid any security risks of putting user content in headers
    # we set a chunk size of 8192 so that the entire file isn't loaded into memory if it's large
    response = StreamingHttpResponse(FileWrapper(open(file_path, 'rb'), 8192), content_type=file_to_serve.mime_type)
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_to_serve.uuid_filename)

    return response


def save_file_to_article(file_to_handle, article):
    """Save a file into an article's folder with appropriate mime type and permissions.

    :param file_to_handle: the uploaded file object we need to handle
    :param article: the article to which the file belongs
    :return: a File object that has been saved in the database
    """

    original_filename = str(file_to_handle.name)

    # N.B. os.path.splitext[1] always returns the final file extension, even in a multi-dotted (.txt.html etc.) input
    filename = str(uuid4()) + str(os.path.splitext(original_filename)[1])
    folder_structure = os.path.join(settings.BASE_DIR, 'files', 'articles', str(article.id))

    save_file_to_disk(file_to_handle, filename, folder_structure)

    file_mime = guess_mime(filename)

    new_file = models   .JamFile(
        mime_type=file_mime,
        original_filename=original_filename,
        uuid_filename=filename,
    )

    return new_file


def save_file_to_disk(file_to_handle, filename, folder_structure):
    """ Save a file to the disk in the specified folder

    :param file_to_handle: the file itself
    :param filename: the filename to save as
    :param folder_structure: the folder structure
    :return: None
    """
    # create the folder structure
    if not os.path.exists(folder_structure):
        os.makedirs(folder_structure)

    path = os.path.join(folder_structure, str(filename))

    # write the file to disk
    with open(path, 'wb') as fd:
        for chunk in file_to_handle.chunks():
            fd.write(chunk)
