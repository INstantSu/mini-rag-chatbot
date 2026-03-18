# Mini RAG Chatbot

A small learning project to understand a chatbot backend with FastAPI, Gemini, RAG, PostgreSQL, Redis, and Celery.

## Current Progress

- FastAPI app skeleton
- Environment settings with `.env`
- SQLModel database connection setup
- Docker Compose with Postgres and Redis
- Initial database models for `documents` and `chat_logs`
- Health check endpoint

## Project Structure

```text
mini-rag-chatbot/
├─ app/
│  ├─ config.py
│  ├─ db.py
│  ├─ main.py
│  └─ models.py
├─ docker-compose.yml
├─ pyproject.toml
└─ README.md
```

## Run

### 1. Install dependencies

```bash
uv sync
```

If `uv` is not available in your shell yet, use:

```bash
~/.local/bin/uv sync
```

### 2. Prepare environment variables

Create a local `.env` file from `.env.example`.

```bash
cp .env.example .env
```

The database URL should use the Docker Postgres port:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/mini_rag
```

### 3. Start Postgres and Redis

```bash
docker compose up -d
```

Check container status:

```bash
docker compose ps
```

Stop containers:

```bash
docker compose down
```

### 4. Run the FastAPI server

```bash
uv run uvicorn app.main:app --reload
```

If `uv` is not available in your shell yet, use:

```bash
~/.local/bin/uv run uvicorn app.main:app --reload
```

### 5. Check the health endpoint

Open:

- `http://127.0.0.1:8000/health`

Or run:

```bash
curl http://127.0.0.1:8000/health
```

### 6. Check database tables

```bash
docker exec mini_rag_postgres psql -U postgres -d mini_rag -c "\dt"
```

Expected tables:

- `documents`
- `chat_logs`
