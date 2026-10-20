---
name: kb-python
description: Portable reference for Python backend development (FastAPI / Django / Flask) — not grounded in this repo. Invoke when a derived project writes or reviews Python endpoints, picks a framework, decides async vs sync, sets type-hint strategy, integrates Pydantic v2, tunes Django ORM, or designs background tasks. For Next.js API contracts → `kb-api`.
last-verified: 2026-04-23
---

# Python — Backend Development

> **Stack:** Python 3.11+ with FastAPI / Django / Flask. Pydantic v2 for validation. pytest for testing.
> **Not grounded in this repo.** TimeKast Factory is Next.js — this skill activates in Python projects that inherit the kit.
> Principles over prescription: choose based on context, don't default.

---

## 1. When to use

**Use for:**

- API-first services (FastAPI + async)
- Full-stack apps with admin (Django)
- Simple scripts or internal tools (Flask / script)
- AI/ML serving (FastAPI + Pydantic + uvicorn)
- Background workers (Celery / ARQ / Dramatiq)

**Don't use for:**

- Next.js server actions → see `kb-api`
- Generic testing principles → see `kb-testing-patterns`
- Data modeling on the Node side → see `kb-db`

---

## 2. Framework selection

```
What are you building?
│
├── API-first / Microservices        → FastAPI (async, modern, fast)
├── Full-stack web / CMS / Admin     → Django (batteries-included)
├── Simple / Script / Learning       → Flask (minimal, flexible)
├── AI/ML API serving                → FastAPI (Pydantic + uvicorn)
└── Background workers               → Celery + any framework
```

| Factor         | FastAPI             | Django          | Flask            |
| -------------- | ------------------- | --------------- | ---------------- |
| Best for       | APIs, microservices | Full-stack, CMS | Simple, learning |
| Async          | Native              | Django 5.0+     | Via extensions   |
| Admin          | Manual              | Built-in        | Via extensions   |
| ORM            | Choose your own     | Django ORM      | Choose your own  |
| Learning curve | Low                 | Medium          | Low              |

**Questions to ask before choosing:**

1. API-only or full-stack?
2. Need admin interface?
3. Team comfortable with async?
4. Existing infra constraints?

---

## 3. Async vs sync

```
I/O-bound       → async (waiting for external)
CPU-bound       → sync + multiprocessing (computing)
```

**Use `async def` when:** I/O-bound (DB, HTTP, file), many concurrent connections, real-time, microservices comms, FastAPI/ASGI.

**Use `def` (sync) when:** CPU-bound, simple scripts, legacy codebase, team unfamiliar with async, blocking libs without async version.

**Never:** mix sync and async carelessly, use sync libs in async code, force async for CPU work.

**Async library map:**

| Need        | Async library                  |
| ----------- | ------------------------------ |
| HTTP client | `httpx`                        |
| PostgreSQL  | `asyncpg`                      |
| Redis       | `aioredis` / `redis-py` async  |
| File I/O    | `aiofiles`                     |
| ORM         | SQLAlchemy 2.0 async, Tortoise |

---

## 4. Type hints

**Always type:**

- Function parameters
- Return types
- Class attributes
- Public APIs

**Can skip:**

- Local variables (let inference work)
- One-off scripts
- Tests (usually)

```python
from typing import Optional, Callable

def find_user(id: int) -> Optional[User]: ...
def process(data: str | dict) -> None: ...
def get_items() -> list[Item]: ...
def apply(fn: Callable[[int], str]) -> str: ...
```

**Pydantic for validation:** API request/response, configuration, data validation, serialization. Runtime validation + auto JSON schema + native FastAPI integration.

---

## 5. Project structure

```
Script:                 Medium API:              Large app:
main.py                 app/                     src/myapp/
utils.py                  __init__.py              core/
requirements.txt          main.py                  api/
                          models/                  services/
                          routes/                  models/
                          services/                ...
                          schemas/               tests/
                        tests/                   pyproject.toml
                        pyproject.toml
```

**FastAPI organization** — by layer (`routes/`, `services/`, `models/`, `schemas/`, `dependencies/`) or by feature (`users/{routes,service,schemas}.py`, `products/...`). Pick one and stick with it.

---

## 6. FastAPI principles

**`async def` vs `def` in endpoints:**

- `async def` — async DB drivers, async HTTP calls, I/O-bound, want concurrency
- `def` — blocking ops, sync drivers, CPU-bound (FastAPI runs in threadpool automatically)

**Pydantic v2 integration:**

```python
@app.post("/users")
async def create(user: UserCreate) -> UserResponse:
    # user is already validated on entry
    # return type becomes response schema
    ...
```

**Dependency injection** — use for DB sessions, current user / auth, configuration, shared resources. Benefits: testability (mock deps), clean separation, automatic cleanup via `yield`.

---

## 7. Django principles (5.0+)

**Async support:** async views, async middleware, async ORM (limited), ASGI deployment. Use for external API calls, WebSocket (Channels), high-concurrency views, background task triggering.

**Model design:** fat models, thin views. Use managers for common queries. Abstract base classes for shared fields.

**Views:** class-based for complex CRUD, function-based for simple endpoints, viewsets with DRF.

**Query discipline:**

```python
# Avoid N+1 queries
Post.objects.select_related('author').all()        # FK → single JOIN
Post.objects.prefetch_related('tags').all()        # M2M → 2 queries
User.objects.only('id', 'email').filter(...)       # Specific fields only
```

---

## 8. Background tasks

| Solution          | Best for                            |
| ----------------- | ----------------------------------- |
| `BackgroundTasks` | Simple, in-process, fire-and-forget |
| Celery            | Distributed, complex workflows      |
| ARQ               | Async, Redis-based                  |
| RQ                | Simple Redis queue                  |
| Dramatiq          | Actor-based, simpler than Celery    |

**Decision:**

- Quick op + same process + no persistence → `BackgroundTasks`
- Long-running + retry + distributed + persistent queue → Celery / ARQ / Dramatiq

---

## 9. Error handling

**Strategy:**

1. Create custom exception classes per domain
2. Register exception handlers (FastAPI `@app.exception_handler`)
3. Return consistent error format
4. Log without exposing internals

**Response shape:**

```json
{
  "code": "USER_NOT_FOUND",
  "message": "User not found",
  "details": { "field": "email" }
}
```

**Never** include stack traces in client-facing errors (security).

**Pattern:** raise domain exceptions in services → catch and transform in handlers → client receives clean response.

---

## 10. Testing

| Type        | Purpose        | Tools                           |
| ----------- | -------------- | ------------------------------- |
| Unit        | Business logic | `pytest`                        |
| Integration | API endpoints  | `pytest` + `httpx`/`TestClient` |
| E2E         | Full workflows | `pytest` + DB                   |

**Async tests:**

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        r = await client.get("/users")
        assert r.status_code == 200
```

**Fixtures:** `db_session`, `client`, `authenticated_user`, `sample_data`.

---

## 11. Decision checklist

Before implementing:

- [ ] Asked user about framework preference?
- [ ] Chosen framework for **this** context (not defaulted)?
- [ ] Decided async vs sync per endpoint?
- [ ] Type hint strategy planned?
- [ ] Project structure chosen (flat / medium / large)?
- [ ] Error handling shape defined?
- [ ] Background task solution selected (if needed)?

---

## 12. Anti-patterns

| ❌ Don't                        | ✅ Do                                  |
| ------------------------------- | -------------------------------------- |
| Default to Django for every API | FastAPI for API-first / async          |
| Sync libraries in async code    | Match sync/async end-to-end            |
| Skip type hints on public APIs  | Always type params + return            |
| Business logic in routes/views  | Routes → Services → Models separation  |
| Ignore N+1 queries              | `select_related` / `prefetch_related`  |
| Force async for CPU work        | Sync + `multiprocessing` for CPU       |
| Expose stack traces in errors   | Clean error response shape             |
| Pydantic models for everything  | Pydantic at boundaries only (req/resp) |

---

_Cross-reference: `kb-api` for the Next.js server-action side. `kb-testing-patterns` for universal test principles._
