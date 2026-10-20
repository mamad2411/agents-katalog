---
name: new-endpoint
description: Scaffold a new FastAPI endpoint with schema, service, repository, and tests
agent: implementer
model: GPT-5.1-Codex
tools:
  - editFiles
  - createFile
  - codebase
  - search
  - problems
  - usages
  - runInTerminal
  - runTests
---

# Create New API Endpoint

## Endpoint: ${input:endpointDescription:Describe the endpoint (e.g., "CRUD for user projects")}

Create a complete FastAPI endpoint following the layered architecture pattern.

### Required Files (create in this order)

1. **Pydantic Schemas** (`backend/app/schemas/`)
   - Request model(s) with field validation
   - Response model(s) with example values
   - Use `ConfigDict(from_attributes=True)` for ORM compatibility

2. **SQLAlchemy Model** (`backend/app/models/`) — if new table needed
   - Use `DeclarativeBase` with `Mapped[T]` annotations
   - Add relationships with `back_populates`
   - Include `created_at` and `updated_at` timestamps

3. **Repository** (`backend/app/repositories/`)
   - Data access methods using `AsyncSession`
   - Use `select()` statements with proper filtering
   - Return typed results: `T | None` for single, `list[T]` for many

4. **Service** (`backend/app/services/`)
   - Business logic layer between routes and repositories
   - Input validation beyond Pydantic (uniqueness checks, authorization)
   - Raise domain exceptions for business rule violations

5. **API Route** (`backend/app/api/v1/`)
   - Use `APIRouter` with tags and prefix
   - Dependency injection with `Annotated[T, Depends()]`
   - OpenAPI metadata: summary, description, response codes
   - Return response models, never raw dicts

6. **Tests** (`backend/tests/`)
   - Happy path tests for each endpoint
   - Validation error tests (422)
   - Not found tests (404)
   - Auth/permission tests (401/403)

### Verify after creation
- Run `#runTests` to ensure all tests pass
- Check `#problems` for type errors
