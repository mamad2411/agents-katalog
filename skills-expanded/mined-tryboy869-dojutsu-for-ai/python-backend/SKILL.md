---
name: python-backend
description: "Apply for any Python backend project: FastAPI, async patterns, structured logging, PostgreSQL with SQLAlchemy 2.0, error handling, and project structure standards."
---

# PYTHON BACKEND — Production Standards 2025

## Structured Logging (NOT print())
```python
import structlog

log = structlog.get_logger()

# Usage — always with context
log.info("job.submitted", job_id=str(job_id), job_type=job_type, user_id=user_id)
log.error("job.failed", job_id=str(job_id), error=str(exc), attempt=attempt)
```

## FastAPI Lifespan (NOT @app.on_event deprecated)
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    await redis_pool.initialize()
    yield
    # Shutdown
    await db.disconnect()
    await redis_pool.close()

app = FastAPI(lifespan=lifespan)
```

## SQLAlchemy 2.0 Async
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=20)

async def get_db():
    async with AsyncSession(engine) as session:
        yield session
```

## Error Handling Pattern
```python
# Domain exceptions, not raw HTTP codes in business logic
class JobNotFound(Exception): pass
class JobQueueFull(Exception): pass

@app.exception_handler(JobNotFound)
async def job_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
```

## Project Structure (standard)
```
src/
├── api/
│   ├── main.py          # FastAPI app + lifespan
│   ├── routes/          # One file per domain
│   └── middleware.py
├── domain/
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── services.py      # Business logic
├── infrastructure/
│   ├── database.py
│   └── redis.py
└── config.py            # pydantic-settings
```

## Type Hints — Always
```python
# Return types on all functions
async def get_job(job_id: UUID) -> JobResponse | None: ...
# Never use Dict, List — use dict, list (Python 3.9+)
async def process_batch(jobs: list[dict]) -> list[str]: ...
```

## Forbidden
❌ `print()` for logging in production code
❌ `@app.on_event("startup")` (deprecated since FastAPI 0.93)
❌ `Session` (sync) instead of `AsyncSession`
❌ Functions without type hints
❌ Catching bare `except Exception` without logging
