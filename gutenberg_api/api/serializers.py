from rest_framework import serializers
from . import models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ('name', 'alias', 'birth_date', 'death_date', 'webpage')


class AgentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgentType
        fields = '__all__'


class AgentSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    type = AgentTypeSerializer()

    class Meta:
        model = models.Agent
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    agents = AgentSerializer(many=True)

    class Meta:
        model = models.Book
        fields = ('id', 'format', 'title', 'description', 'downloads', 'license', 'subjects',
                  'bookshelves', 'languages', 'agents', 'resources')


class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bookshelf
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = ('name',)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ('name',)


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = ('uri', 'type', 'size', 'modified')
