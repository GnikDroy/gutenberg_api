from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.routers import APIRootView

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from . import models
from . import serializers


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for books.
    """
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    filter_backends = (filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('title', 'agents__person__name')

    class BookFilter(django_filters.FilterSet):
        type = django_filters.CharFilter(
            field_name="type", lookup_expr="exact")
        languages = django_filters.ModelChoiceFilter(
            queryset=models.Language.objects.all())
        title_contains = django_filters.CharFilter(
            field_name="title", lookup_expr="icontains")
        description_contains = django_filters.CharFilter(
            field_name="description", lookup_expr="icontains")
        downloads_range = django_filters.NumericRangeFilter(
            field_name="downloads", lookup_expr="range")
        has_bookshelf = django_filters.CharFilter(
            field_name="bookshelves__name", lookup_expr="exact")
        has_resource_type = django_filters.CharFilter(
            field_name="resources__type", lookup_expr="exact")
        has_agent_type = django_filters.CharFilter(
            field_name="agents__type", lookup_expr="exact")
        agent_name_contains = django_filters.CharFilter(
            field_name="agents__person__name", lookup_expr="icontains")
        agent_alias_contains = django_filters.CharFilter(
            field_name="agents__person__alias", lookup_expr="icontains")
        agent_webpage_contains = django_filters.CharFilter(
            field_name="agents__person__webpage", lookup_expr="icontains")
        agent_birth_date_range = django_filters.NumericRangeFilter(
            field_name="agents__person__birth_date", lookup_expr="range")
        agent_death_date_range = django_filters.NumericRangeFilter(
            field_name="agents__person__death_date", lookup_expr="range")

        class Meta:
            model = models.Book
            fields = []

    filterset_class = BookFilter

    ordering_fields = ('downloads', 'title')


class BookshelfViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and view details for Bookshelves.
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
    List and view details Person objects.
    """
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer
    filter_backends = (filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('name', 'alias')

    class PersonFilter(django_filters.FilterSet):
        name_contains = django_filters.CharFilter(
            field_name="name", lookup_expr="icontains")
        alias_contains = django_filters.CharFilter(
            field_name="alias", lookup_expr="icontains")
        webpage_contains = django_filters.CharFilter(
            field_name="webpage", lookup_expr="icontains")
        birth_date_range = django_filters.NumericRangeFilter(
            field_name="birth_date", lookup_expr="range")
        death_date_range = django_filters.NumericRangeFilter(
            field_name="death_date", lookup_expr="range")

        class Meta:
            model = models.Person
            fields = []

    filterset_class = PersonFilter
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

    class AgentFilter(django_filters.FilterSet):
        type = django_filters.ModelChoiceFilter(
            queryset=models.AgentType.objects.all())
        name_contains = django_filters.CharFilter(
            field_name="person__name", lookup_expr="icontains")
        birth_date = django_filters.NumericRangeFilter(
            field_name="person__birth_date", lookup_expr="range")
        death_date = django_filters.NumericRangeFilter(
            field_name="person__death_date", lookup_expr="range")

        class Meta:
            model = models.Agent
            fields = []

    filterset_class = AgentFilter
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

    class ResourceFilter(django_filters.FilterSet):
        size_gt = django_filters.NumberFilter(
            field_name='size', lookup_expr='gt')
        size_lt = django_filters.NumberFilter(
            field_name='size', lookup_expr='lt')
        size_range = django_filters.NumericRangeFilter(
            field_name='size', lookup_expr='range')

        modified_gt = django_filters.DateFilter(
            field_name='modified', lookup_expr='gt')
        modified_lt = django_filters.DateFilter(
            field_name='modified', lookup_expr='lt')
        modified_range = django_filters.DateFromToRangeFilter(
            field_name='modified', lookup_expr='range')

        type = django_filters.CharFilter(
            field_name='type', lookup_expr='exact')

        class Meta:
            model = models.Resource
            fields = []

    filterset_class = ResourceFilter

    ordering_fields = ('size', 'modified')


class ProjectGutenbergAPIRootView(APIRootView):
    """
    Select the endpoints for more information on each.
    """
