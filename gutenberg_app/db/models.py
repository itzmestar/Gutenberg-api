from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from gutenberg_app.db.db_connect import Base


class Author(Base):
    __tablename__ = 'books_author'
    id = Column(Integer, primary_key=True)
    birth_year = Column(Integer)
    death_year = Column(Integer)
    name = Column(String(128), nullable=False)

    books = relationship('BookAuthor', back_populates='author')


class Book(Base):
    __tablename__ = 'books_book'
    id = Column(Integer, primary_key=True)
    download_count = Column(Integer, default=0)
    gutenberg_id = Column(Integer, unique=True, nullable=False)
    media_type = Column(String(16), nullable=False)
    title = Column(String(1024))

    authors = relationship('BookAuthor', back_populates='book')
    bookshelves = relationship('BookBookshelf', back_populates='book')
    languages = relationship('BookLanguage', back_populates='book')
    subjects = relationship('BookSubject', back_populates='book')
    formats = relationship('BookFormat', back_populates='book')


class BookAuthor(Base):
    __tablename__ = 'books_book_authors'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('books_author.id'), nullable=False)

    book = relationship('Book', back_populates='authors')
    author = relationship('Author', back_populates='books')


class BookBookshelf(Base):
    __tablename__ = 'books_book_bookshelves'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'), nullable=False)
    bookshelf_id = Column(Integer, ForeignKey('books_bookshelf.id'), nullable=False)

    book = relationship('Book', back_populates='bookshelves')


class BookLanguage(Base):
    __tablename__ = 'books_book_languages'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'), nullable=False)
    language_id = Column(Integer, ForeignKey('books_language.id'), nullable=False)

    book = relationship('Book', back_populates='languages')


class BookSubject(Base):
    __tablename__ = 'books_book_subjects'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('books_subject.id'), nullable=False)

    book = relationship('Book', back_populates='subjects')


class Bookshelf(Base):
    __tablename__ = 'books_bookshelf'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)


class BookFormat(Base):
    __tablename__ = 'books_format'
    id = Column(Integer, primary_key=True)
    mime_type = Column(String(32), nullable=False)
    url = Column(String(256), nullable=False)
    book_id = Column(Integer, ForeignKey('books_book.id'), nullable=False)

    book = relationship('Book', back_populates='formats')


class Language(Base):
    __tablename__ = 'books_language'
    id = Column(Integer, primary_key=True)
    code = Column(String(4), nullable=False)


class Subject(Base):
    __tablename__ = 'books_subject'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
