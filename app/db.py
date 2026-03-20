from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings
from app import models


engine = create_engine(settings.database_url, echo=True)


def create_db_and_tables() -> None:
    with engine.begin() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
