import json
from pathlib import Path

from google import genai
from google.genai import types

from sqlmodel import Session

from app.config import settings
from app.db import engine
from app.models import Document


BASE_DIR = Path(__file__).resolve().parent.parent
SEED_FILE = BASE_DIR / "seed_data" / "wellness_docs.json"

client = genai.Client(api_key=settings.gemini_api_key)


def load_seed_documents():
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=768),
    )
    return response.embeddings[0].values


def main():
    docs = load_seed_documents()

    with Session(engine) as session:
        for item in docs:
            embedding = generate_embedding(item["content"])

            document = Document(
                title=item["title"],
                content=item["content"],
                embedding=embedding,
            )
            session.add(document)

        session.commit()

    print(f"Inserted {len(docs)} documents.")


if __name__ == "__main__":
    main()
