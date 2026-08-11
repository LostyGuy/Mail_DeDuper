from pathlib import Path

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.app.paths import BASE_DIR 

SQLLITE_DATABASE_URL = f"sqlite:///{Path(BASE_DIR, "lists_of", "list_of_shared_emails.db")}"

Engine = create_engine(SQLLITE_DATABASE_URL)
SessionLocal = sessionmaker(bind= Engine, autoflush= False, autocommit= False,)
Base = declarative_base()

Base.metadata.create_all(Engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    