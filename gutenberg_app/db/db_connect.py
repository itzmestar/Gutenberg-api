from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from gutenberg_app.config.constants import (
    DB_HOST, DB_USER, DB_PASS, DB_NAME
)

# database url
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Create a db connection session & close the connection after execution
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
