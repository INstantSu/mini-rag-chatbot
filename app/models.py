from datetime import datetime, timezone
from typing import List, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    embedding: Optional[List[float]] = Field(
        default=None,
        sa_column=Column(Vector(768), nullable=True),
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatLog(SQLModel, table=True):
    __tablename__ = "chat_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_question: str
    answer: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
