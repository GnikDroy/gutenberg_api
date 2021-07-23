"""Management command to load initial catalog data from database

Contains functions to load the initial catalogue from database
Also registers a django management command named 'load_db' that can be
used as `python manage.py load_db`
"""

import logging
import os
import sys
import sqlite3
from datetime import datetime
import pytz

from django.core.exceptions import FieldError
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from api import models


def clear_db() -> None:
    """Clears all catalogue related information present in the database.

    NOTE: This does not remove images from the media/ directory.

    Returns:
        None
    """
    models.Person.objects.all().delete()
    models.AgentType.objects.all().delete()
    models.Agent.objects.all().delete()
    models.Bookshelf.objects.all().delete()
    models.Language.objects.all().delete()
    models.Subject.objects.all().delete()
    models.Resource.objects.all().delete()
    models.Book.objects.all().delete()


def import_catalogue(logger, fixture_file_path: str, clear: bool) -> None:
    """Imports the catalogue from fixtures.

    Imports all database information from the fixture path.
    This function can clear all database information.

    Args:
        logger: The logger used to log messages.
        fixture_file_path: the path to the fixture file.
        clear (bool): Whether to clear the database before import.

    Returns:
        None
    """
    # Clear catalogue if instructed
    if clear:
        clear_db()
        logger.info("Cleared database")

    if not os.path.exists(fixture_file_path):
        logger.error("Fixture file not found. Nothing imported.")

    conn = sqlite3.connect(fixture_file_path)
    cur = conn.cursor()

    logger.info("Populating Book")
    cur.execute("""
    SELECT id, format, title, description, license, downloads FROM Book
    """)
    books = cur.fetchall()
    book_objs = []
    for id, format, title, description, license, downloads in books:
        book_objs.append(models.Book(id=id, format=format, title=title,
                         description=description, license=license, downloads=downloads))
    models.Book.objects.bulk_create(book_objs)
    book_objs.clear()

    logger.info("Populating Person")
    cur.execute("""
    SELECT id, name, alias, birth_date, death_date, webpage FROM Person;
    """)
    people = cur.fetchall()
    people_objs = []
    for id, name, alias, birth_date, death_date, webpage in people:
        people_objs.append(models.Person(
            pk=id, name=name, alias=alias, birth_date=birth_date, death_date=death_date, webpage=webpage))
    models.Person.objects.bulk_create(people_objs)
    people_objs.clear()

    logger.info("Populating AgentType")
    cur.execute("""
    SELECT name FROM AgentType;
    """)
    agent_types = cur.fetchall()
    agent_type_objs = []
    for name, in agent_types:
        agent_type_objs.append(models.AgentType(name=name))
    models.AgentType.objects.bulk_create(agent_type_objs)
    agent_type_objs.clear()

    logger.info("Populating Agent")
    cur.execute("""
    SELECT id, person, type FROM Agent;
    """)
    agents = cur.fetchall()
    agent_objs = []
    for agent_id, person_id, type_id in agents:
        agent_objs.append(models.Agent(pk=agent_id, person_id=person_id, type_id=type_id))
    models.Agent.objects.bulk_create(agent_objs)
    agent_objs.clear()

    logger.info("Populating Bookshelf")
    cur.execute("""
    SELECT name FROM Bookshelf
    """)
    bookshelves = cur.fetchall()
    bookshelf_objs = []
    for name, in bookshelves:
        bookshelf_objs.append(models.Bookshelf(name=name))
    models.Bookshelf.objects.bulk_create(bookshelf_objs)
    bookshelf_objs.clear()

    logger.info("Populating Subject")
    cur.execute("""
    SELECT name FROM Subject
    """)
    subjects = cur.fetchall()
    subject_objs = []
    for name, in subjects:
        subject_objs.append(models.Subject(name=name))
    models.Subject.objects.bulk_create(subject_objs)
    subject_objs.clear()

    logger.info("Populating Resource")
    cur.execute("""
    SELECT url, size, modified, type FROM Resource
    """)
    resources = cur.fetchall()
    resource_objs = []
    for url, size, modified_str, type in resources:
        modified_str = modified_str.split(".")[0]
        modified = datetime.strptime(
            modified_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
        resource_objs.append(models.Resource(
            uri=url, size=size, modified=modified, type=type))
    models.Resource.objects.bulk_create(resource_objs)
    resource_objs.clear()

    logger.info("Populating Language")
    cur.execute("""
    SELECT name FROM Language
    """)
    languages = cur.fetchall()
    language_objs = []
    for name, in languages:
        language_objs.append(models.Language(name=name))
    models.Language.objects.bulk_create(language_objs)

    logger.info("Populating Book Language M2M relation")
    cur.execute("""
    SELECT book, language FROM Book_Language;
    """)
    book_languages = cur.fetchall()
    LanguageThrough = models.Book.languages.through
    languages_through = []
    for book_id, language_id in book_languages:
        languages_through.append(LanguageThrough(
            book_id=book_id, language_id=language_id))
    LanguageThrough.objects.bulk_create(languages_through)
    languages_through.clear()

    logger.info("Populating Book Subject M2M relation")
    cur.execute("""
    SELECT book, subject FROM Book_Subject;
    """)
    book_subject = cur.fetchall()
    SubjectThrough = models.Book.subjects.through
    subjects_through = []
    for book_id, subject_id in book_subject:
        subjects_through.append(SubjectThrough(
            book_id=book_id, subject_id=subject_id))
    SubjectThrough.objects.bulk_create(subjects_through)
    subjects_through.clear()

    logger.info("Populating Book Resource M2M relation")
    cur.execute("""
    SELECT book, resource FROM Book_Resource;
    """)
    book_resource = cur.fetchall()
    ResourceThrough = models.Book.resources.through
    resources_through = []
    for book_id, resource_id in book_resource:
        resources_through.append(ResourceThrough(
            book_id=book_id, resource_id=resource_id))
    ResourceThrough.objects.bulk_create(resources_through)
    resources_through.clear()

    logger.info("Populating Book Bookshelf M2M relation")
    cur.execute("""
    SELECT book, bookshelf FROM Book_Bookshelf;
    """)
    book_bookshelf = cur.fetchall()
    BookshelfThrough = models.Book.bookshelves.through
    bookshelves_through = []
    for book_id, bookshelf_id in book_bookshelf:
        bookshelves_through.append(BookshelfThrough(
            book_id=book_id, bookshelf_id=bookshelf_id))
    BookshelfThrough.objects.bulk_create(bookshelves_through)
    bookshelves_through.clear()

    logger.info("Populating Book Agent M2M relation")
    cur.execute("""
    SELECT book, agent FROM Book_Agent;
    """)
    book_agent = cur.fetchall()
    AgentThrough = models.Book.agents.through
    agents_through = []
    for book_id, agent_id in book_agent:
        agents_through.append(AgentThrough(book_id=book_id, agent_id=agent_id))
    AgentThrough.objects.bulk_create(agents_through)
    agents_through.clear()

    cur.close()
    conn.close()

    logger.info("Database import complete")


class Command(BaseCommand):
    """Django management command for load_db"""
    help = 'For importing book catalogue from fixtures.'

    def add_arguments(self, parser) -> None:
        """Add arguments to load_db

        Args:
            parser: django command line parser

        Returns:
            None
        """
        parser.add_argument('path', help='/path/to/fixture.sqlite3')

        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing entries in the catalogue before import"
        )

    def handle(self, *args, **options) -> None:
        """Django management handler for load_catalogue.

        Inherited member. See django docs for more details.
        """
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)

        logger = logging.getLogger('api.load_db')
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        import_catalogue(logger, options["path"], options["clear"])
