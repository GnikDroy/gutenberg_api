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


class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bookshelf
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = ('id', 'uri', 'type', 'size', 'modified')


class BookSerializer(serializers.ModelSerializer):
    subjects = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    bookshelves = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class BookAgentSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        person = serializers.SlugRelatedField(read_only=True, slug_field="name")
        type = serializers.SlugRelatedField(read_only=True, slug_field="name")
    agents = BookAgentSerializer(many=True)

    class BookResourceSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        uri = serializers.URLField()
        type = serializers.CharField()
    resources = BookResourceSerializer(many=True)

    class Meta:
        model = models.Book
        fields = ('id', 'type', 'title', 'description', 'downloads', 'license', 'subjects',
                  'bookshelves', 'languages', 'agents', 'resources')
