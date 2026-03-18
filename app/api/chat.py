from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import get_session
from app.models import ChatLog
from app.schemas import ChatRequest, ChatResponse
from app.services.llm_service import generate_chat_answer


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, session: Session = Depends(get_session)):
    answer = generate_chat_answer(request.question)

    chat_log = ChatLog(
        user_question=request.question,
        answer=answer,
    )
    session.add(chat_log)
    session.commit()

    return ChatResponse(answer=answer)
