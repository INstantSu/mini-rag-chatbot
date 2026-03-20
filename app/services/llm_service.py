from google import genai

from app.config import settings


client = genai.Client(api_key=settings.gemini_api_key)

# @param context: RAG 컨텍스트
def generate_chat_answer(question: str, context: str = "") -> str:
    prompt = f"""
You are a small educational mental wellness chatbot.
Give supportive and simple educational information.
Do not present yourself as a medical or therapeutic system.
Use the retrieved documents when they are relevant.
If the documents are not enough, answer carefully and briefly.

Retrieved documents:
{context}

User question:
{question}
""".strip()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text or "Sorry, I could not generate a response."
