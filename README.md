# Mini RAG Chatbot

FastAPI, Gemini, PostgreSQL + pgvector, Redis, Celery로 만든 작은 학습용 RAG 챗봇 백엔드 프로젝트입니다.

이 프로젝트의 목적은 아래 기술이 각각 어떤 역할을 하는지 직접 확인하는 것입니다.

- LLM
- RAG
- PostgreSQL + pgvector
- Redis
- Celery worker
- Docker Compose

이 프로젝트는 의료 진단이나 치료를 제공하는 시스템이 아닙니다. 심리 및 웰빙 관련 일반 교육용 정보를 다루는 학습용 예제입니다.

## RAG 적용 전후 비교

### Before RAG
![Before RAG](docs/images/before-rag.png)

### After RAG
![After RAG](docs/images/after-rag.png)

## 현재 구현 범위

- `GET /health`
- `POST /chat`
  - 사용자 질문 embedding 생성
  - pgvector 유사도 검색
  - 검색 문서를 Gemini 프롬프트에 포함
  - 최종 답변 생성 및 `chat_logs` 저장
- `POST /documents`
  - 새 문서 저장
  - Celery task enqueue
  - worker가 백그라운드에서 embedding 생성 후 `documents.embedding` 업데이트
- seed 문서 적재 스크립트
- Docker Compose로 `api`, `worker`, `postgres`, `redis` 실행

## 기술 스택

- Python
- FastAPI
- SQLModel
- Gemini API
- PostgreSQL + pgvector
- Redis
- Celery
- uv
- Docker Compose

## 프로젝트 구조

```text
mini-rag-chatbot/
├─ app/
│  ├─ api/
│  │  ├─ chat.py
│  │  └─ documents.py
│  ├─ services/
│  │  ├─ embedding_service.py
│  │  ├─ llm_service.py
│  │  └─ rag_service.py
│  ├─ worker/
│  │  ├─ celery_app.py
│  │  └─ tasks.py
│  ├─ config.py
│  ├─ db.py
│  ├─ main.py
│  ├─ models.py
│  └─ schemas.py
├─ scripts/
│  └─ seed_documents.py
├─ seed_data/
│  ├─ README.md
│  └─ wellness_docs.json
├─ Dockerfile
├─ docker-compose.yml
├─ pyproject.toml
└─ README.md
```

## 환경 변수

`.env.example`을 복사해서 `.env` 파일을 만듭니다.

```bash
cp .env.example .env
```

예시:

```env
APP_NAME=Mini RAG Chatbot
APP_ENV=dev
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/mini_rag
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=your_gemini_api_key_here
```

로컬에서 직접 실행할 때는 `localhost:5433`을 사용합니다.  
Docker Compose 안의 `api`, `worker` 컨테이너는 `docker-compose.yml`에서 `postgres:5432`, `redis:6379`를 사용하도록 별도 설정되어 있습니다.

## 실행 방법

### 1. 의존성 설치

```bash
uv sync
```

`uv`가 PATH에 없다면:

```bash
~/.local/bin/uv sync
```

### 2. 전체 스택 실행

```bash
docker compose up --build
```

백그라운드 실행:

```bash
docker compose up --build -d
```

상태 확인:

```bash
docker compose ps
```

중지:

```bash
docker compose down
```

DB까지 초기화:

```bash
docker compose down -v
```

## seed 문서 적재

초기 RAG 문서를 DB에 넣으려면:

```bash
PYTHONPATH=. uv run python scripts/seed_documents.py
```

이 스크립트는 `seed_data/wellness_docs.json`을 읽어서:

- 문서를 `documents` 테이블에 저장하고
- Gemini embedding을 생성해서
- `documents.embedding`에 저장합니다.

## API 테스트

### health check

```bash
curl http://127.0.0.1:8000/health
```

### 채팅 요청

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question":"잠이 잘 안 오고 머리가 복잡할 때 기본적으로 무엇을 해볼 수 있을까?"}'
```

### 새 문서 추가

```bash
curl -X POST "http://127.0.0.1:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Simple Reset Note",
    "content": "A short pause can help when thoughts feel crowded. Notice your breathing, your shoulders, and one sound around you."
  }'
```

## 데이터 확인

테이블 목록:

```bash
docker exec mini_rag_postgres psql -U postgres -d mini_rag -c "\dt"
```

문서 목록:

```bash
docker exec mini_rag_postgres psql -U postgres -d mini_rag -c "SELECT id, title FROM documents ORDER BY id;"
```

embedding 생성 여부:

```bash
docker exec mini_rag_postgres psql -U postgres -d mini_rag -c "SELECT id, title, embedding IS NOT NULL AS has_embedding FROM documents ORDER BY id DESC LIMIT 10;"
```

채팅 로그:

```bash
docker exec mini_rag_postgres psql -U postgres -d mini_rag -c "SELECT id, user_question, created_at FROM chat_logs ORDER BY id DESC LIMIT 10;"
```

## 요청 흐름

`/chat` 요청 흐름:

1. 사용자가 질문을 보냅니다.
2. API가 질문 embedding을 생성합니다.
3. PostgreSQL + pgvector에서 유사한 문서 top-k를 찾습니다.
4. 검색된 문서를 Gemini 프롬프트에 포함합니다.
5. Gemini가 최종 답변을 생성합니다.
6. 답변을 `chat_logs`에 저장합니다.
7. 사용자에게 응답을 반환합니다.

## 백그라운드 흐름

`/documents` 요청 흐름:

1. 사용자가 새 문서를 보냅니다.
2. API가 문서를 `documents` 테이블에 저장합니다.
3. API가 Celery task를 Redis 큐에 넣습니다.
4. worker가 task를 가져옵니다.
5. worker가 문서 embedding을 생성합니다.
6. worker가 `documents.embedding`을 업데이트합니다.

## 이 프로젝트에서 각 기술의 역할

- `FastAPI`: HTTP API 서버
- `Gemini`: 답변 생성과 embedding 생성
- `RAG`: 내부 문서를 검색해서 LLM에 참고 자료로 제공
- `PostgreSQL`: 문서와 채팅 로그 저장
- `pgvector`: embedding 저장과 유사도 검색
- `Redis`: Celery 작업 큐
- `Celery`: 백그라운드 embedding 작업 처리
- `SQLModel`: DB 모델과 세션 관리
- `Docker Compose`: 로컬 전체 스택 실행
