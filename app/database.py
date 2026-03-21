"""
Database setup using SQLAlchemy ORM
Connects to MySQL and provides a session for each request
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# create engine with connection pooling
# pool_pre_ping checks if connection is alive before using it (handles mysql timeout issues)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Creates a new database session for each request
    and closes it after the request is done.
    Used as a FastAPI dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
