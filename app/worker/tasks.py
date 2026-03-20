import logging

from sqlmodel import Session, select

from app.db import engine
from app.models import Document
from app.services.embedding_service import generate_embedding
from app.worker.celery_app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task
def generate_document_embedding(document_id: int) -> None:
    logger.info("Starting embedding task for document_id=%s", document_id)

    with Session(engine) as session:
        statement = select(Document).where(Document.id == document_id)
        document = session.exec(statement).first()

        if document is None:
            logger.warning("Document not found for document_id=%s", document_id)
            return

        logger.info("Generating embedding for document_id=%s", document_id)
        document.embedding = generate_embedding(document.content)

        logger.info("Saving embedding for document_id=%s", document_id)
        session.add(document)
        session.commit()

    logger.info("Finished embedding task for document_id=%s", document_id)
