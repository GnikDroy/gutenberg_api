from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.routers import APIRootView
from . import models
from . import serializers 

# Create your views here.

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for books.
    """
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer

class BookshelfViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Bookshelfs.
    """
    queryset = models.Bookshelf.objects.all()
    serializer_class = serializers.BookshelfSerializer

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Subjects.
    """
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer

class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Languages.
    """
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer

class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Persons.
    """
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer

class AgentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Agent Types.
    """
    queryset = models.AgentType.objects.all()
    serializer_class = serializers.AgentTypeSerializer

class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Agents.
    """
    queryset = models.Agent.objects.all()
    serializer_class = serializers.AgentSerializer

class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Resources.
    """
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer
    
class ProjectGutenbergAPIRootView(APIRootView):
    """
    Select the endpoints for more information on each.
    """