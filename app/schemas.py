from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


class DocumentCreate(BaseModel):
    title: str
    content: str


class DocumentRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
