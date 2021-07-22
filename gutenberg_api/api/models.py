from django.db import models

# Create your models here.

MAX_UNKNOWN_LENGTH = 1000


class Person(models.Model):
    name = models.CharField(max_length=MAX_UNKNOWN_LENGTH)
    alias = models.CharField(max_length=MAX_UNKNOWN_LENGTH)
    birth_date = models.CharField(max_length=MAX_UNKNOWN_LENGTH)
    death_date = models.CharField(max_length=MAX_UNKNOWN_LENGTH)
    webpage = models.URLField()

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return f"{self.name}"


class AgentType(models.Model):
    name = models.CharField(max_length=MAX_UNKNOWN_LENGTH, primary_key=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return f"{self.name}"


class Agent(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    type = models.ForeignKey(AgentType, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        if Person.objects.filter(pk=self.person).exists():
            return f"{Person.objects.get(pk=self.person).name}"
        else:
            return f"Agent: [{self.person}, {self.type}]"


class Bookshelf(models.Model):
    name = models.CharField(max_length=MAX_UNKNOWN_LENGTH, primary_key=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return f"{self.name}"


class Language(models.Model):
    name = models.CharField(max_length=MAX_UNKNOWN_LENGTH, primary_key=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return f"{self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=MAX_UNKNOWN_LENGTH, primary_key=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return f"{self.name}"


class Resource(models.Model):
    uri = models.URLField(primary_key=True)
    size = models.IntegerField()
    modified = models.DateTimeField()
    type = models.CharField(max_length=500)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    format = models.CharField(max_length=MAX_UNKNOWN_LENGTH)
    title = models.CharField(max_length=MAX_UNKNOWN_LENGTH)
    description = models.CharField(max_length=MAX_UNKNOWN_LENGTH)
    license = models.URLField()
    downloads = models.IntegerField()

    subjects = models.ManyToManyField(Subject)
    bookshelves = models.ManyToManyField(Bookshelf)
    languages = models.ManyToManyField(Language)
    resources = models.ManyToManyField(Resource)
    agents = models.ManyToManyField(Agent)

    class Meta:
        ordering = ('-downloads',)

    def __str__(self):
        return f"{self.title}"
