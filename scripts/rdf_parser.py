#!/usr/bin/env python3

import rdflib
import os
import json
import argparse

def xstr(s):
    return None if s is None else str(s)

class Book:
    BASE = rdflib.Namespace("http://www.gutenberg.org/")
    DC_TERMS = rdflib.Namespace("http://purl.org/dc/terms/")
    PG_TERMS = rdflib.Namespace("http://www.gutenberg.org/2009/pgterms/")
    RDF = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    RDFS = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
    CC = rdflib.Namespace("http://web.resource.org/cc/")
    DCAM = rdflib.Namespace("http://purl.org/dc/dcam/")
    MACREL = rdflib.Namespace("http://id.loc.gov/vocabulary/relators/")


    @staticmethod
    def parse_agent(graph, agent):
        return {
            "name": xstr(graph.value(agent, Book.PG_TERMS["name"])),
            "alias": xstr(graph.value(agent, Book.PG_TERMS["alias"])),
            "birth_date": xstr(graph.value(agent, Book.PG_TERMS["birthdate"])),
            "death_date": xstr(graph.value(agent, Book.PG_TERMS["deathdate"])),
            "webpage": xstr(graph.value(agent, Book.PG_TERMS["webpage"]))
        }

    @staticmethod
    def parse_book(graph, id):
        book = {}
        book_id = Book.BASE[f"ebooks/{id}"]

        book["id"] = id

        book["format"] = xstr(graph.value(graph.value(
            book_id, Book.DC_TERMS["type"]), Book.RDF["value"]))

        book["title"] = xstr(graph.value(book_id, Book.DC_TERMS["title"]))

        book["publishers"] = list(
            map(xstr, graph.objects(book_id, Book.DC_TERMS["publisher"])))

        book["description"] = xstr(graph.value(
            book_id, Book.DC_TERMS["description"]))

        book["downloads"] = xstr(graph.value(
            book_id, Book.PG_TERMS["downloads"]))

        book["license"] = xstr(graph.value(book_id, Book.DC_TERMS["license"]))

        book["subjects"] = []
        for subject_hash in graph.objects(book_id, Book.DC_TERMS["subject"]):
            book["subjects"].append(
                xstr(graph.value(subject_hash, Book.RDF["value"])))

        book["resources"] = []
        for url in graph.objects(book_id, Book.DC_TERMS["hasFormat"]):
            size = xstr(graph.value(url, Book.DC_TERMS["extent"]))
            last_modified = xstr(graph.value(url, Book.DC_TERMS["modified"]))
            file_type = xstr(graph.value(graph.value(
                url, Book.DC_TERMS["format"]), Book.RDF["value"]))
            book["resources"].append({
                "url": xstr(url),
                "size": size,
                "modified": last_modified,
                "type": file_type,
            })

        book["languages"] = []
        for language_hash in graph.objects(book_id, Book.DC_TERMS["language"]):
            book["languages"].append(
                xstr(graph.value(language_hash, Book.RDF["value"])))

        book["bookshelves"] = []
        for bookshelf_hash in graph.objects(book_id, Book.PG_TERMS["bookshelf"]):
            book["bookshelves"].append(
                xstr(graph.value(bookshelf_hash, Book.RDF["value"])))

        book["agents"] = {}

        authors = []
        for author in graph.objects(book_id, Book.DC_TERMS["creator"]):
            authors.append(Book.parse_agent(graph, author))
        book["agents"]["Author"] = authors

        for predicate, agent in graph.predicate_objects(book_id):
            assert isinstance(predicate, rdflib.URIRef)
            type_names = {
                "ann": "Annotator",
                "cmm": "Commentator",
                "cmp": "Composer",
                "com": "Compiler",
                "ctb": "Contributor",
                "edt": "Editor",
                "ill": "Illustrator",
                "oth": "Other",
                "pht": "Photographer",
                "trl": "Translator",
            }

            if predicate.startswith(Book.MACREL):
                name = None
                for id, value in type_names.items():
                    if predicate == Book.MACREL[id]:
                        name = value

                book["agents"].setdefault(xstr(name), []).append(
                    Book.parse_agent(graph, agent))

        return book

    @staticmethod
    def parse(id, input_file):
        graph = rdflib.Graph().parse(input_file)
        return Book.parse_book(graph, id)

    @staticmethod
    def convert_to_json(id, input_file, output_file):
        if not os.path.exists(output_file):
            book = Book.parse(id, input_file)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", newline="\n") as f:
                json.dump(book, f)


def main(args):
    for path, _, filenames in os.walk(args.input):
        for filename in filenames:
            if filename.endswith(".rdf"):
                try:
                    id = int(os.path.basename(path))
                    input_file = os.path.join(path, filename)
                    output_file = os.path.join(args.output, f"{id}.json")
                    Book.convert_to_json(id, input_file, output_file)
                    print(f"Converted book: {id}")
                except ValueError:
                    print(f"Error: Cannot convert file named '{os.path.basename(path)}' to integer")
                    continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Convert RDF files to JSON format for faster parsing.")
    parser.add_argument("-i",
                        "--input", help="The input RDF directory.",
                        default="res/rdf")
    parser.add_argument(
        "-o", "--output", help="The output JSON directory", default="res/json")
    main(parser.parse_args())
