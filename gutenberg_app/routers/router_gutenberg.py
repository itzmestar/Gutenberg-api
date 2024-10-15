from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from gutenberg_app.db.db_connect import get_db
from gutenberg_app.db.models import Book, BookLanguage, Language
from gutenberg_app.config.constants import QUERY_RESPONSE_SIZE
from sqlalchemy import desc


# create an api-router
router = APIRouter(
    prefix="/gutenberg",
    tags=["gutenberg"],
)


class BookResponse:
    title: str
    authors: List[str]
    genres: List[str]
    language: str
    subjects: List[str]
    bookshelves: List[str]
    download_links: List[dict]


@router.get("/books/")
def get_books(
    db: Session = Depends(get_db),
    offset: int = 0
):
    """
    List the books based on the given filter criteria
    """
    query = db.query(Book).join(BookLanguage).join(Language).order_by(desc(Book.download_count))

    # count total no. of books found as result of the query
    total_books = query.count()
    books = query.offset(offset).limit(QUERY_RESPONSE_SIZE).all()

    return {
        "total": total_books,
        "books": [
            {
                "title": book.title,
                "authors": [author.name for author in book.authors],
                "genres": [bookshelf.name for bookshelf in book.bookshelves],
                "language": [language.code for language in book.languages],
                "subjects": [subject.name for subject in book.subjects],
                "bookshelves": [bookshelf.name for bookshelf in book.bookshelves],
                "download_links": [{"mime_type": format.mime_type, "url": format.url} for format in book.formats]
            }
            for book in books
        ]
    }
