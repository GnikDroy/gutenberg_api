#!/usr/bin/env python3

import sqlite3
import os
import json
import argparse

import rdf_parser


class BookDB:

    def __init__(self, path):
        self.path = path
        self.connection = None
        self.cursor = None

    def open(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        return self

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.close()

    def create_tables(self):
        self.cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Book (
            id INTEGER PRIMARY KEY,
            format TEXT,
            title TEXT,
            description TEXT,
            license TEXT,
            downloads INTEGER
        );

        CREATE TABLE IF NOT EXISTS AgentType (
            name TEXT PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS Person (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT,
            alias TEXT,
            birth_date TEXT,
            death_date TEXT,
            webpage TEXT,
            UNIQUE(name, alias, birth_date, death_date, webpage)
        );

        CREATE TABLE IF NOT EXISTS Agent (
            person INTEGER,
            type TEXT,
            FOREIGN KEY (person) REFERENCES Person(id),
            FOREIGN KEY (type) REFERENCES AgentType(name),
            PRIMARY KEY (person, type)
        );
        
        CREATE TABLE IF NOT EXISTS Bookshelf (
            name TEXT PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS Subject (
            name TEXT PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS Language (
            name TEXT PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS Resource (
            url TEXT PRIMARY KEY,
            size INTEGER,
            modified TEXT,
            type TEXT
        );

        CREATE TABLE IF NOT EXISTS Book_Subject (
            book INTEGER,
            subject TEXT,
            FOREIGN KEY (book) REFERENCES Book(id),
            FOREIGN KEY (subject) REFERENCES Subject(name),
            PRIMARY KEY (book, subject)
        );

        CREATE TABLE IF NOT EXISTS Book_Agent (
            book INTEGER,
            agent_person INTEGER,
            agent_type INTEGER,
            FOREIGN KEY (book) REFERENCES Book(id),
            FOREIGN KEY (agent_person, agent_type) REFERENCES Agent(person, type),
            PRIMARY KEY (book, agent_person, agent_type)
        );

        CREATE TABLE IF NOT EXISTS Book_Resource (
            book INTEGER,
            resource TEXT,
            FOREIGN KEY (book) REFERENCES Book(id),
            FOREIGN KEY (resource) REFERENCES Resource(url),
            PRIMARY KEY (book, resource)
        );


        CREATE TABLE IF NOT EXISTS Book_Language (
            book INTEGER,
            language TEXT,
            FOREIGN KEY (book) REFERENCES Book(id),
            FOREIGN KEY (language) REFERENCES Language(name),
            PRIMARY KEY (book, language)
        );

        CREATE TABLE IF NOT EXISTS Book_Bookshelf (
            book INTEGER,
            bookshelf TEXT,
            FOREIGN KEY (book) REFERENCES Book(id),
            FOREIGN KEY (bookshelf) REFERENCES Bookshelf(name),
            PRIMARY KEY (book, bookshelf)
        );''')

    def insert_book(self, book):
        self.cursor.execute("""
        INSERT OR REPLACE INTO Book (id, format, title, description, license, downloads) VALUES (?, ?, ?, ?, ?, ?)
        """, (book["id"], book["format"], book["title"], book["description"], book["license"], int(book["downloads"])))
        book_row_id = self.cursor.lastrowid

        for resource in book['resources']:
            self.cursor.execute("""
            INSERT OR REPLACE INTO Resource (url, size, modified, type) VALUES (?, ?, ?, ?)
            """, (resource["url"], resource["size"], resource["modified"], resource["type"]))

            self.cursor.execute("""
            INSERT OR REPLACE INTO Book_Resource (book, resource) VALUES (?, ?)
            """, (book_row_id, resource["url"]))

        for agent_type, agents in book["agents"].items():
            self.cursor.execute("""
            INSERT OR REPLACE INTO AgentType (name) VALUES (?)
            """, (agent_type,))

            for agent in agents:
                self.cursor.execute("""
                INSERT OR IGNORE INTO Person (name, alias, birth_date, death_date, webpage) VALUES (?, ?, ?, ?, ?)
                """, (agent["name"], agent["alias"], agent["birth_date"], agent["death_date"], agent["webpage"]))
                self.cursor.execute("""
                SELECT id from Person
                WHERE 
                name=? AND alias=? AND birth_date=? AND death_date=? AND webpage=?
                """, (agent["name"], agent["alias"], agent["birth_date"], agent["death_date"], agent["webpage"]))
                person_id = self.cursor.fetchone()[0]

                self.cursor.execute("""
                INSERT OR REPLACE INTO Agent (person, type) VALUES (?, ?)
                """, (person_id, agent_type))

                self.cursor.execute("""
                INSERT OR REPLACE INTO Book_Agent (book, agent_person, agent_type) VALUES (?, ?, ?)
                """, (book_row_id, person_id, agent_type))

        for bookshelf in book["bookshelves"]:
            self.cursor.execute("""
            INSERT OR REPLACE INTO Bookshelf (name) VALUES (?)
            """, (bookshelf,))

            self.cursor.execute("""
            INSERT OR REPLACE INTO Book_Bookshelf (book, bookshelf) VALUES (?, ?)
            """, (book_row_id, bookshelf))

        for subject in book["subjects"]:
            self.cursor.execute("""
            INSERT OR REPLACE INTO Subject (name) VALUES (?)
            """, (subject,))

            self.cursor.execute("""
            INSERT OR REPLACE INTO Book_Subject (book, subject) VALUES (?, ?)
            """, (book_row_id, subject))

        for lang in book["languages"]:
            self.cursor.execute("""
            INSERT OR REPLACE INTO Language (name) VALUES (?)
            """, (lang,))

            self.cursor.execute("""
            INSERT OR REPLACE INTO Book_Language (book, language) VALUES (?, ?)
            """, (book_row_id, lang))


def main(args):
    with BookDB(args.output) as book_db:
        book_db.create_tables()
        for path, _, filenames in os.walk(args.input_rdf):
            for _ in filenames:
                id = int(os.path.basename(path))
                book = {}

                # Prefer the json formats due to speed.
                if os.path.exists(os.path.join(args.input_json, f"{id}.json")):
                    with open(os.path.join(args.input_json, f"{id}.json")) as f:
                        book = json.load(f)
                else:
                    book = rdf_parser.Book.parse(
                        id, str(os.path.join(args.input_rdf, f"{id}/pg{id}.rdf")))

                book_db.insert_book(book)
                print(f'Inserted book: {book["id"]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Create sqlite database for project gutenberg from RDF or JSON files.")
    parser.add_argument("-r",
                        "--input_rdf", help="The directory that contains the RDF files (formatted similar to how Project Gutenberg presents it.)",
                        default="res/rdf")
    parser.add_argument(
        "-j", "--input_json", help="The directory that contains the converted JSON files. (Use this for faster generation.)", default="res/json")
    parser.add_argument(
        "-o", "--output", help="The output database path", default="books.sqlite3")
    main(parser.parse_args())
