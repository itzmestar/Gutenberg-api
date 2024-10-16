from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from gutenberg_app.db.db_connect import get_db
from gutenberg_app.db.models import (
    Book, BookLanguage, Language, Author, BookAuthor, Bookshelf, Subject, BookFormat, BookBookshelf, BookSubject
)
from gutenberg_app.config.constants import QUERY_RESPONSE_SIZE
from sqlalchemy import desc, or_
from sqlalchemy.inspection import inspect
import logging


# create an api-router
router = APIRouter(
    prefix="/gutenberg",
    tags=["gutenberg"],
)


# Function to convert model instance to dict
def model_to_dict(model):
    return {c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs}


@router.get("/books/")
def get_books(
    db: Session = Depends(get_db),
    gutenberg_ids: Optional[List[int]] = Query(None),
    languages: Optional[List[str]] = Query(None),
    mime_types: Optional[List[str]] = Query(None),
    topics: Optional[List[str]] = Query(None),
    authors: Optional[List[str]] = Query(None),
    titles: Optional[List[str]] = Query(None),
    offset: int = 0
):
    """
    List the books based on the given filter criteria
    """
    query = db.query(Book).order_by(desc(Book.download_count))

    # filter results by gutenberg_ids
    if gutenberg_ids:
        query = query.filter(Book.gutenberg_id.in_(gutenberg_ids))

    # filter results by languages
    if languages:
        query = query.join(BookLanguage).join(Language).filter(Language.code.in_(languages))

    # Filter by MIME types (e.g., text/html, application/pdf)
    if mime_types:
        logging.info(mime_types)
        query = query.join(BookFormat).filter(BookFormat.mime_type.in_(mime_types))

    # Filter by topics (subjects or bookshelves)
    if topics:
        # Join and filter by bookshelves
        query = query.join(BookBookshelf).join(Bookshelf).filter(
            or_(*[Bookshelf.name.ilike(f"%{topic}%") for topic in topics])
        )
        # Join and filter by subjects
        query = query.join(BookSubject).join(Subject).filter(
            or_(*[Subject.name.ilike(f"%{topic}%") for topic in topics])
        )

    # Filter by authors (partial, case-insensitive match)
    if authors:
        author_filters = [Author.name.ilike(f"%{author}%") for author in authors]
        query = query.join(BookAuthor).join(Author).filter(or_(*author_filters))

    # If titles are provided, apply case-insensitive partial match for each
    if titles:
        title_filters = [Book.title.ilike(f"%{title}%") for title in titles]
        query = query.filter(or_(*title_filters))  # Use `or_` to match any title

    # count total no. of books found as result of the query
    total_books = query.count()
    books = query.offset(offset).limit(QUERY_RESPONSE_SIZE).all()

    #logging.info(model_to_dict(books[0].bookshelves[0]))

    return {
        "total": total_books,
        "books": [
            {
                "title": book.title,
                "downloads": book.download_count,
                "authors info": [{
                    "name": author.author.name,
                    "birth": author.author.birth_year,
                    "death": author.author.death_year
                } for author in book.authors],
                "genres": [subject.subject.name for subject in book.subjects],
                "language": [language.language.code for language in book.languages],
                "subjects": [subject.subject.name for subject in book.subjects],
                "bookshelves": [bookshelf.bookshelf.name for bookshelf in book.bookshelves],
                "download_links": [{"mime_type": format.mime_type, "url": format.url} for format in book.formats]
            }
            for book in books
        ]
    }
