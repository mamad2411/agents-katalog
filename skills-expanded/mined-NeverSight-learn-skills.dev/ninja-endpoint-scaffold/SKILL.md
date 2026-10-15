---
name: ninja-endpoint-scaffold
description: Scaffold Django Ninja API endpoints with proper service-layer separation, Reply response wrappers, exception hierarchies, and test skeletons for the data-support-platform project. Use when the user asks to implement a new API endpoint, create a RESTful route, design request/response schemas, plan an API feature, or add CRUD operations.
---

# Django Ninja API Endpoint Scaffold

> For architecture-layer rules (API/Service/Business separation) and coding standards, see `AGENTS.md` §1–5.
> For testing and debugging patterns, load the `django-ninja-testing` skill.
> For complete working examples, check the project directory:
> - **If `repo/` exists**: Reference `repo/full-stack-fastapi-template/backend/app/api/routes/` for FastAPI routing patterns and `repo/full-stack-fastapi-template/backend/app/crud.py` for CRUD separation patterns.
> - **If `repo/` does NOT exist**: Reference `openspec/changes/archive/2026-01-07-improve-llm-coding-rules/` for Django Ninja examples (`example_api.py`, `example_service.py`, `example_exception_registration.py`).

---

## Workflow: Plan → Scaffold → Implement → Test

### Step 1: Plan (User Approval Required)

Before writing code, produce a structured implementation plan:

1. **Request/Response JSON Schemas** (pydantic V2, `model_config` not `class Config`)
2. **HTTP Status Code Matrix** (200/201/207/400/404/409/422/500)
3. **Service Method Signature** (input DTO → output/exception)
4. **Exception Types** (custom service exceptions + registration in `SheetManage/exceptions.py`)
5. **Mermaid Flowchart** (for multi-step workflows)
6. **Test Skeleton** (API integration + service unit tests)

> **Query Context7** for Django 4.2 and Django Ninja 1.3 documentation before designing schemas.

### Step 2: Scaffold

Generate these 4 files in order:

| # | File | Purpose |
|---|------|---------|
| 1 | `sheetScript/services/{name}_service.py` | Custom exceptions + DTOs + Service class |
| 2 | `sheetScript/api/{name}_api.py` | Router + Schemas + Endpoint functions |
| 3 | `SheetManage/api.py` | Add `api.add_router()` + exception imports |
| 4 | `SheetManage/exceptions.py` | Register exception handlers |

### Step 3: Implement

Follow this layer order: **Service → API → Exception Registration**.

**Service Layer rules:**
- Throw custom exceptions for errors, never return error dicts
- Use `@transaction.atomic` for multi-step DB operations
- Define DTO classes for complex inputs (e.g., `CreateParams`)
- Log at `info` for success, `warning` for client errors, `error` for server errors

**API Layer rules:**
- `return Reply(data=...)` for success (not `200, Reply(...)`)
- `return 201, Reply(...)` for created
- `return FileResponse(...)` directly (no Reply wrapper)
- Let service exceptions propagate — do not catch them
- Use `@wrap_reply()` for endpoints with pagination

### Step 4: Test

Load the `django-ninja-testing` skill and generate:
- Service layer unit tests (success + error paths)
- API layer integration tests with `TestClient(main_api)` singleton
- Exception propagation tests (verify correct HTTP status codes)

---

## Quick Reference

### Response Patterns

```python
# Success (200)
return Reply(data=ItemOut.from_orm(item))

# Created (201)
return 201, Reply(data=IdOut(id=item_id), info="Created")

# File download (no Reply)
return FileResponse(open(path, "rb"), filename="file.xlsx")

# Error — throw in service, let propagate
raise ItemNotFoundError(f"Item {id} not found")
```

### Exception Status Codes

| Status | Use for |
|--------|---------|
| 400 | Validation errors, bad request parameters |
| 401 | Authentication failures (expired/invalid token) |
| 403 | Permission denied |
| 404 | Resource not found |
| 409 | Conflicts (duplicate task, concurrent modification) |
| 422 | Processing errors (file format, schema mismatch) |
| 425 | Too early (task not yet completed) |
| 500 | Internal service errors |

### pydantic V2 Schema Config

```python
# CORRECT (pydantic V2)
class MyOut(Schema):
    model_config = {"from_attributes": True}

# WRONG (pydantic V1)
class MyOut(Schema):
    class Config:
        from_attributes = True
```

### Sub-router Registration

```python
# api.py
router = Router(auth=AuthBearer())
subrouter = Router(auth=AuthBearer())
router.add_router(prefix="/comparison/", router=subrouter)

api.add_router("/items/", router, tags=["items"])
```

### Pagination

```python
@wrap_reply()
@paginate(ReplyPagination)
def list_items(request, filters: FilterSchema = Query(...)):
    service = ItemService()
    return service.get_items(filters)
```

---

## Detailed Reference

See [REFERENCE.md](REFERENCE.md) for:
- Complete API/Service/Exception registration examples
- Anti-patterns to avoid
- Common scenarios and solutions
- Implementation checklists
