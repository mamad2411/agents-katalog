# FastAPI Skill

You are working on a FastAPI project. Apply these conventions.

## Project Structure

```
app/
├── main.py            # FastAPI app creation, router inclusion
├── routers/           # APIRouter groupings by domain
├── models/            # SQLAlchemy / database models
├── schemas/           # Pydantic request/response schemas
├── dependencies/      # Reusable Depends() functions
├── services/          # Business logic layer
└── core/              # Settings, security, database session
```

## App Setup

- Create the FastAPI app once and include routers: `app.include_router(users.router, prefix="/users", tags=["users"])`.
- Use `lifespan` for startup/shutdown logic (not deprecated `on_event`):
  ```python
  from contextlib import asynccontextmanager
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      # startup
      yield
      # shutdown
  app = FastAPI(lifespan=lifespan)
  ```

## Pydantic Models (v2)

- Use Pydantic v2 — `model_config = ConfigDict(from_attributes=True)` replaces `class Config: orm_mode = True`.
- Separate schemas for creation (`UserCreate`), update (`UserUpdate`), and response (`UserResponse`).
- Use `model_validator` and `field_validator` (not `@validator` — that's v1 syntax).

## Dependency Injection

- Create reusable dependencies with `Depends()`:
  ```python
  async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
  ```
- Inject database sessions via `Depends(get_db)` — never create sessions inside route handlers.

## Async

- Use `async def` for route handlers that perform I/O (DB, HTTP).
- Use `def` (synchronous) for CPU-bound handlers — FastAPI runs them in a thread pool.
- Use `asyncpg` or `SQLAlchemy` async engine for async DB operations.

## Error Handling

- Raise `HTTPException(status_code=404, detail="Not found")` for expected errors.
- Use exception handlers for global errors: `@app.exception_handler(RequestValidationError)`.
- Return consistent error shapes — define a base `ErrorResponse` Pydantic schema.

## Security

- Validate all input via Pydantic — FastAPI rejects invalid payloads automatically (422).
- Never trust header values directly for auth — validate JWTs with `python-jose` or `authlib`.
- Use `SecretStr` from Pydantic for secret values in settings.
- Enable CORS only for known origins via `CORSMiddleware`.
