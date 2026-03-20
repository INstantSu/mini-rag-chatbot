from sqlmodel import Session, select

from app.db import engine
from app.models import Document
from app.services.embedding_service import generate_embedding
from app.worker.celery_app import celery_app


@celery_app.task
def generate_document_embedding(document_id: int) -> None:
    with Session(engine) as session:
        statement = select(Document).where(Document.id == document_id)
        document = session.exec(statement).first()

        if document is None:
            return

        document.embedding = generate_embedding(document.content)
        session.add(document)
        session.commit()
