from django.shortcuts import get_object_or_404

from JamStore import files, models


def serve_article_file(request, identifier, file_id):
    """ Serves an article file.

    :param request: the request associated with this call
    :param identifier_type: the identifier type for the article
    :param identifier: the identifier for the article
    :param file_id: the file ID to serve
    :return: a streaming response of the requested file or 404
    """
    article_object = models.Jam.objecs.get(pk=identifier)
    file_object = get_object_or_404(models.JamFile, pk=file_id)

    return files.serve_file(request, file_object, article_object)
