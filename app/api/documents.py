from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import get_session
from app.models import Document
from app.schemas import DocumentCreate, DocumentRead


router = APIRouter()


@router.post("/documents", response_model=DocumentRead)
def create_document(
    request: DocumentCreate,
    session: Session = Depends(get_session),
):
    document = Document(
        title=request.title,
        content=request.content,
    )

    session.add(document)
    session.commit()
    session.refresh(document)

    return DocumentRead(
        id=document.id,
        title=document.title,
        content=document.content,
        created_at=document.created_at,
    )
