---
name: openapi-fastapi
description: OpenAPI spec generation with FastAPI and Pydantic models
user-invocable: false
stack: api-docs/openapi-fastapi
paths:
  - "**/main.py"
  - "**/routers/*.py"
  - "**/schemas/*.py"
  - "**/dependencies.py"
  - "**/api/**/*.py"
  - "**/openapi*"
---

Full standards in [openapi-fastapi.md](openapi-fastapi.md). Always-on summary:

**Spec Generation:**
- FastAPI auto-generates `/openapi.json` and `/docs` (Swagger UI) — never hand-write specs
- Set `title`, `version`, `description`, and `contact` in the `FastAPI()` constructor
- Group routes with `APIRouter(prefix=..., tags=[...])` so spec is organized by domain

**Pydantic Models as Schemas:**
- Every request body and response model must be a `BaseModel` subclass
- Use `Field(...)` for descriptions, examples, and constraints — they appear in the spec
- Define separate `Create`, `Update`, and `Read` schemas; never reuse the same model for all operations
- Use `model_config = ConfigDict(from_attributes=True)` for ORM models

**Security Schemes:**
- Declare `OAuth2PasswordBearer` or `HTTPBearer` in a central `security.py` — inject via `Depends()`
- Add `security=[{"bearerAuth": []}]` at router level, not per-endpoint
- Document scopes in the scheme definition when using OAuth2

**Response Models:**
- Always set `response_model=` on every route decorator
- Use `response_model_exclude_unset=True` to avoid leaking default `None` fields
- Return `JSONResponse` only for error overrides; let FastAPI serialize Pydantic models

**Never:**
- Mount routes without `tags` — the spec becomes one unnavigable blob
- Return `dict` from a route that has a `response_model` — bypass causes schema drift
- Expose internal fields (passwords, secrets) in response models
- Skip `status_code=201` on `POST` routes or `status_code=204` on `DELETE` routes — always declare explicitly

**Related skills:** `api-conventions`, `error-handling`, `database-sql`
