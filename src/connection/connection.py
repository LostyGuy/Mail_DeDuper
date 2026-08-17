from pathlib import Path

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.app.paths import BASE_DIR


DATABASE_PATH = Path("/app/data/mail_deduper.db")
SQLLITE_DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

Engine = create_engine(SQLLITE_DATABASE_URL)
SessionLocal = sessionmaker(bind= Engine, autoflush= False, autocommit= False,)

Base = declarative_base()
def database_initialization():
    from src.connection import models
    #!---- ----
    # Base.metadata.drop_all(Engine)
    #!---- ----
    Base.metadata.create_all(Engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    