from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.routers import APIRootView

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from . import models
from . import serializers

# Create your views here.


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for books.
    """
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    filter_backends = (filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('title', 'agents__person__name')
    filterset_fields = ('type', 'languages', 'bookshelves')
    ordering_fields = ('downloads', 'title')


class BookshelfViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Bookshelfs.
    """
    queryset = models.Bookshelf.objects.all()
    serializer_class = serializers.BookshelfSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', )
    ordering_fields = ('name', )


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Subjects.
    """
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', )
    ordering_fields = ('name', )


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Languages.
    """
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', )
    ordering_fields = ('name', )


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Persons.
    """
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer
    filter_backends = (filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('name', 'alias')
    filterset_fields = ('birth_date', 'death_date')
    ordering_fields = ('name', 'alias', 'birth_date', 'death_date')


class AgentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Agent Types.
    """
    queryset = models.AgentType.objects.all()
    serializer_class = serializers.AgentTypeSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', )
    ordering_fields = ('name', )


class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Agents.
    """
    queryset = models.Agent.objects.all()
    serializer_class = serializers.AgentSerializer
    filter_backends = (filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('person__name', 'person__alias', 'type__name')
    filterset_fields = ('type', )
    ordering_fields = ('person__name', 'person__alias',
                       'person__birth_date', 'person__death_date')


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Resources.
    """
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer
    filter_backends = (filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('uri', )
    filterset_fields = ('size', 'type')
    ordering_fields = ('size', 'modified')


class ProjectGutenbergAPIRootView(APIRootView):
    """
    Select the endpoints for more information on each.
    """
