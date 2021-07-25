from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings

from api import models
import os


MARKDOWN_FILES = {}


def lazy_load_markdown(path, toc=True, reload=True):
    """
    Use this to keep markdown files in memory.

    :param path: The path to the Markdown file from BASE_DIR
    :param toc: Generation of Table of Contents
    :param reload: Whether to reload the markdown file on every call. Useful for debug.
    """
    if reload or not path in MARKDOWN_FILES:
        with open(path) as f:
            prefix = "[TOC] \n" if toc else ""
            MARKDOWN_FILES[path] = prefix + f.read()


def index(request):
    """
    The Homepage
    """
    template = loader.get_template('main/index.html')
    context = {
        "books": models.Book.objects.all().count(),
        "creators": models.Person.objects.all().count(),
        "bookshelves": models.Bookshelf.objects.all().count(),
        "subjects": models.Subject.objects.all().count(),
        "resources": models.Resource.objects.all().count(),
        "languages": models.Language.objects.all().count(),
    }
    return HttpResponse(template.render(context, request))


def docs(request):
    """
    The Documentation Page
    """
    template = loader.get_template('main/markdown.html')
    markdown_path = os.path.join(settings.BASE_DIR, "DOCS.md")
    lazy_load_markdown(markdown_path)
    return HttpResponse(template.render({"markdown_html": MARKDOWN_FILES[markdown_path]}, request))
