from django.shortcuts import render

from rest_framework import viewsets
from . import models
from . import serializers 

# Create your views here.

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer

class BookshelfViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Bookshelf.objects.all()
    serializer_class = serializers.BookshelfSerializer

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer

class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer

class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer

class AgentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.AgentType.objects.all()
    serializer_class = serializers.AgentTypeSerializer

class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Agent.objects.all()
    serializer_class = serializers.AgentSerializer

class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer