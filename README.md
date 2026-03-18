# Mini RAG Chatbot

A small learning project to understand a chatbot backend with FastAPI, Gemini, RAG, PostgreSQL, Redis, and Celery.

## Step 1
- FastAPI app skeleton
- Environment settings
- Database connection placeholder
- Docker Compose with Postgres and Redis

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
