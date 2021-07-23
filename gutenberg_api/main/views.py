from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from api import models

# Create your views here.
def index(request):
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