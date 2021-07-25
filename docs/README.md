# Installation and Setup

An instance should be running [here][Site]. Please host your own instance if you are planning on using the API extensively.

To host your own, firstly **clone the repository.**

```sh
git clone <repository>
```

You will need to generate the SQLite Database from the Project Gutenberg catalogue. The catalogue is updated daily and is not present in the repository.

**Get a copy of the Project Gutenberg catalog** [here](https://www.gutenberg.org/cache/epub/feeds/). We use the [format](https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.zip) where each book gets its own RDF file. The current implementation of RDF in python has poor performance so parsing the single file catalogue is not feasible.

Once you have the catalogue, you can use `scripts/rdf_parser.py` or `scripts/books_db.py` to **generate the JSON catalogue or an SQLite database**. Since RDFLib has poor performance, it is often worthwhile to convert the RDF files to JSON with `rdf_parser.py`, and use `books_db.py` to finally generate the SQLite database. If you do not need to do this regularly, `books_db.py` will also directly create an SQLite database from the RDF files.

```sh
pip install -r scripts/requirements.txt
[python] rdf_parser.py -h
[python] books_db.py -h
```

 You should be able to generate a SQLite database after reading the help messages. Additionally, you have the ability to generate JSON files if need be.

*This will take some time!* Get yourself a cup of coffee.

After generating a SQLite database, you will need to **load this into Django**. There is a custom `load_db` command inside `api` app for this.

Before that, let's setup the django project. From your project root:

```sh
pip install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py makemigrations api
python3 manage.py migrate

# python3 manage.py createsuperuser # Create a super user account. This might be unnecessary for your needs.
```

Finally, let's load the generated SQLite DB

```sh
python3 manage.py load_db [--clear] path/to/generated_sqlite.db

# For more info: python3 manage.py load_db -h
```

## Deployment

Setup your environment,

```sh
cp .env.template .env
```

You should populate `.env` with your production settings (SECRET_KEYS, ALLOWED_HOSTS, etc). If you are not in production, the default settings will set you up for development. You do not need to do anything.

Additionally, if you are in production you might have to setup some stuff in `wsgi.py` or `asgi.py`. Please refer to the [django docs](https://docs.djangoproject.com/en/dev/howto/deployment/) for more details.

After setting everything up, you should be ready to roll!

```sh
python3 manage.py runserver <PORT>
```


*I am unable to test installation steps for every single environment. If you have had to perform some additional steps to reach this stage, and would like to inform others, please create a PR.*

_______________

## Details

*This section is NOT for you if you only want to quickly setup and deploy the app.*

### Generated SQLite Database

The generated SQLite database can be used differently.  You should be able to see the tables from some sort of a DB management software. Please refer to `scripts/books_db.py` for more details on the format.

### Mirroring the site

If you are aiming to make a lot of requests to the `Resource` obtained from the API, it might be worthwhile to [mirror Project Gutenberg.](https://www.gutenberg.org/help/mirroring.html). You would then need to update the Resource URIs generated from the RDF files to point to your domain. Refer to `books_db.py` and `rdf_parser.py`. A small SQLite command will also do the job.

_______________

# API Reference

It is highly recommended to use the [Browseable API][API] to interact with the API instead.

## Endpoints

The following endpoints are currently supported. 

|    Endpoint     | Details                                              |
|:---------------:|:-----------------------------------------------------|
|    /api/book    | Details of a Book                                    |
| /api/bookshelf  | Bookshelf information                                |
| /api/agent_type | The type of agent. (Artist, Illustrator, etc)        |
|   /api/person   | Details of a person (name, birth date, webpage, etc) |
|  /api/resource  | Details of a resource (url, size, type, etc)         |
|   /api/agent    | Agent is a unique (Person, AgentType) pair           |
|  /api/language  | Language of the book (en, fr, etc)                   |
|  /api/subject   | The list of genres/subjects.                         |

_______________

### Basics

The endpoints can be used to **list** and to **view details** of an item.

Pagination applies for viewing the list of items. For instance, to view the list of Books.

```python
GET /api/book/

{
    "count": 65777,
    "next": "<next_page_url>",
    "previous": null,
    "results": [...]
}

# count = Total number of books
# next = URL for the next page
# previous = URL for the previous page
# results = Array of Book instances.
```

Provide the id to view the details of a model. This might be an integer or a string.

For instance, the following GET request would return the details of a book.

```python
GET /api/book/21558/

{
    "id": 21558,
    "type": "Text",
    "title": "The Children of the New Forest",
    "description": null,
    "downloads": 164,
    "license": "http://www.gutenberg.org/license",
    "subjects": [
        "Foresters -- Juvenile fiction",
        "New Forest (England : Forest) -- Juvenile fiction",
        "Great Britain -- History -- Civil War, 1642-1649 -- Juvenile fiction",
        "Soldiers -- Juvenile fiction",
        "Orphans -- Juvenile fiction",
        "PZ"
    ],
    "bookshelves": [],
    "languages": [ "en" ],
    "agents": [
        {
            "id": 3570,
            "person": "Marryat, Frederick",
            "type": "Author"
        }
    ],
    "resources": [
        {
            "id": 182146,
            "uri": "https://www.gutenberg.org/files/21558/21558.zip",
            "type": "application/zip"
        },
        {
            "id": 182145,
            "uri": "https://www.gutenberg.org/ebooks/21558.kindle.noimages",
            "type": "application/x-mobipocket-ebook"
        },
    ]
}
```

Note that this applies to all endpoints. So `/api/person/1` would show details of a particular person.

_______________

### Search, Filter and Order

#### Search

For search you can use the `?search=` query parameter to search for items.

For instance,

```python
GET /api/book/?search=Jane

{
    "count": 288,
    "next": "...",
    "previous": null,
    "results": [...]
}
```

_______________

#### Filter

Reasonable filters are available at most endpoints. For instance, `?languages=` available at the `Book` endpoint.

```python
GET /api/book/?languages=en

{
    "count": 53265,
    "next": "/api/book/?languages=en&page=2",
    "previous": null,
    "results": [
        {
            "id": 1342,
            "format": "Text",
            "title": "Pride and Prejudice",
            ...
        },
        ...
    ]
}
```

Here are some of the filters available:

|   Model    | Filters                                                                                                                                                                                                                                     |
|:----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   `Book`   | type, languages, title_contains, description_contains, downloads_range, has_bookshelf, has_resource_type, has_agent_type, agent_name_contains, agent_alias_contains, agent_webpage_contains, agent_birth_date_range, agent_death_date_range |
|  `Person`  | name_contains, alias_contains, webpage_contains, birth_date_range, death_date_range                                                                                                                                                         |
|  `Agent`   | type, name_contains, birth_date, death_date                                                                                                                                                                                                 |
| `Resource` | size_gt, size_lt, size_range, modified_gt, modified_lt, modified_range, type                                                                                                                                                                |

The suffixes have intuitive meanings:

|   Suffix    | Meaning                                                                                                                               |
|:-----------:|:--------------------------------------------------------------------------------------------------------------------------------------|
|    `gt`     | Greater than (Number, Date, String etc)                                                                                               |
|    `lt`     | Less than (Number, Date, String etc)                                                                                                  |
| `contains`  | Case insensitive search on the field                                                                                                  |
|   `range`   | Creates max and min query pairs for range based filtering. For example `size_range` will create `size_range_min` and `size_range_max` |
| `NO SUFFIX` | Usually an exact match filter. Might have different meaning depending on the context.                                                 |

Please refer to the [Browseable API][API] for a comprehensive list of filters available at each endpoint.

_______________

#### Ordering

Similar to filters, reasonable ordering mechanisms are available at most endpoints.

```python
GET /api/book/?ordering=-downloads

{
    "count": 65777,
    "next": "/api/book/?ordering=-downloads&page=2",
    "previous": null,
    "results": [
        {
            "id": 1342,
            "format": "Text",
            "title": "Pride and Prejudice",
            "description": "https://en.wikipedia.org/wiki/Pride_and_Prejudice",
            "downloads": 43379,
            ...
        },
        ...
    ]
}
```

Notice how `?ordering=-downloads` orders results in a descending order whereas `?ordering=downloads` in an ascending order. You can also order them by multiple fields. For instance, `?ordering=-downloads,title` will work as well.

Please refer the [Browseable API][API] for a more comprehensive list of orderings available at each endpoint.

*As expected, Search, Filters and Ordering  queries can be combined.*

_______________

# Contributing Guidelines

Feel free to raise a new [issue][Github] or send a [pull request][Github].

Any contribution is welcome. That being said, please raise an issue before you start working on a new feature.

_______________

# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, caste, color, religion, or sexual identity
and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment for our
community include:

* Demonstrating empathy and kindness toward other people
* Being respectful of differing opinions, viewpoints, and experiences
* Giving and gracefully accepting constructive feedback
* Accepting responsibility and apologizing to those affected by our mistakes,
  and learning from the experience
* Focusing on what is best not just for us as individuals, but for the
  overall community

Examples of unacceptable behavior include:

* The use of sexualized language or imagery, and sexual attention or
  advances of any kind
* Trolling, insulting or derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or email
  address, without their explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Enforcement Responsibilities

Community leaders are responsible for clarifying and enforcing our standards of
acceptable behavior and will take appropriate and fair corrective action in
response to any behavior that they deem inappropriate, threatening, offensive,
or harmful.

Community leaders have the right and responsibility to remove, edit, or reject
comments, commits, code, wiki edits, issues, and other contributions that are
not aligned to this Code of Conduct, and will communicate reasons for moderation
decisions when appropriate.

## Scope

This Code of Conduct applies within all community spaces, and also applies when
an individual is officially representing the community in public spaces.
Examples of representing our community include using an official e-mail address,
posting via an official social media account, or acting as an appointed
representative at an online or offline event.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders responsible for enforcement.

All complaints will be reviewed and investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of the
reporter of any incident.

## Enforcement Guidelines

Community leaders will follow Community Impact Guidelines in determining
the consequences for any action they deem in violation of this Code of Conduct.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][Contributor_Covenant_Homepage],
version 2.0, available at [Code of Conduct][Code_Of_Conduct].

Community Impact Guidelines were inspired by [Mozilla's code of conduct enforcement ladder][Mozilla_CoC].

For answers to common questions about this code of conduct, see the FAQ at
[FAQ][Contributor_Covenant_FAQ]. Translations are available [here][Contributor_Covenant_Translations].

[Contributor_Covenant_Homepage]: https://www.contributor-covenant.org
[Code_Of_Conduct]: https://www.contributor-covenant.org/version/2/0/code_of_conduct.html
[Mozilla_CoC]: https://github.com/mozilla/diversity
[Contributor_Covenant_FAQ]: https://www.contributor-covenant.org/faq
[Contributor_Covenant_Translations]: https://www.contributor-covenant.org/translations
_______________

# About

The Gutenberg API is one of the largest source of free ebooks, and the catalogue provides a lot of metadata. The existing projects did not fully expose all the information provided in the metadata (this project aims to provide most of the relevant ones). Additionally, we also provide a mechanism to parse the RDF files into JSON or an SQLite database for easier analysis, as well as a comprehensive browsable API view.

## Similar Projects

* [garethbjohnson / gutendex](https://github.com/garethbjohnson/gutendex)
* [c-w / gutenberg-http](https://github.com/c-w/gutenberg-http/)

_______________

# License

You can find the license at [Github][Github]. Please refer to [Project Gutenberg's policy](https://www.gutenberg.org/policy/license.html) on the use of resources made available to you.

[Github]: https://www.github.com/GnikDroy/gutenberg_api
[Site]: https://gnikdroy.pythonanywhere.com
[API]: https://gnikdroy.pythonanywhere.com/api