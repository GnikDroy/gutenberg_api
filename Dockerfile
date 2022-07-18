FROM python:3-alpine
WORKDIR /app

COPY . .
ADD https://github.com/GnikDroy/gutenberg_api/releases/download/1.0.1%2Bdb/books.sqlite3.xz books.sqlite3.xz

RUN unxz books.sqlite3.xz &&\
    pip install -r requirements.txt &&\
    python manage.py migrate &&\
    python manage.py load_db --clear books.sqlite3 &&\
    rm books.sqlite3

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000