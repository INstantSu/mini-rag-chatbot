from sqlalchemy import text
from sqlmodel import Session

from app.models import Document
from app.services.embedding_service import generate_embedding
from app.services.llm_service import generate_chat_answer


def _to_vector_literal(values: list[float]) -> str:
    return "[" + ",".join(str(value) for value in values) + "]"


def retrieve_documents(question: str, session: Session, top_k: int = 3) -> list[Document]:
    question_embedding = generate_embedding(question)
    question_embedding_literal = _to_vector_literal(question_embedding)

    statement = text(
        """
        SELECT id, title, content, embedding, created_at
        FROM documents
        ORDER BY embedding <=> CAST(:question_embedding AS vector)
        LIMIT :top_k
        """
    )

    rows = session.exec(
        statement,
        params={
            "question_embedding": question_embedding_literal,
            "top_k": top_k,
        },
    ).all()

    documents = []
    for row in rows:
        documents.append(
            Document(
                id=row.id,
                title=row.title,
                content=row.content,
                embedding=row.embedding,
                created_at=row.created_at,
            )
        )

    return documents


def build_context(documents: list[Document]) -> str:
    parts = []

    for index, doc in enumerate(documents, start=1):
        parts.append(f"[Document {index}]")
        parts.append(f"Title: {doc.title}")
        parts.append(f"Content: {doc.content}")
        parts.append("")

    return "\n".join(parts).strip()


def generate_rag_answer(question: str, session: Session) -> str:
    documents = retrieve_documents(question, session=session, top_k=3)
    context = build_context(documents)
    return generate_chat_answer(question=question, context=context)
