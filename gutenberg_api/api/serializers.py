from rest_framework import serializers
from . import models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = '__all__'


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
        fields = '__all__'
