---
name: django-ninja-testing
description: Write and troubleshoot Django Ninja API endpoint tests. Use when the user asks to write tests for Django Ninja APIs, encounters TestClient ConfigError, needs to test authenticated endpoints, wants test patterns for ninja routers/operations, needs to diagnose a Django/Ninja runtime error, or wants to audit test coverage.
---

# Django Ninja API Testing & Diagnosis

> For architecture-layer rules (API/Service/Business separation, Reply/Response patterns, exception handling), see `AGENTS.md` §1–3.

---

## Quick start

```python
# tests/sheetScript/test_my_api.py
import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SheetManage.settings")
sys.path.insert(0, ".")
import django; django.setup()

from ninja.testing import TestClient
from SheetManage.api import api as main_api

# CRITICAL: TestClient is a process-wide singleton.
# Creating it more than once raises
#   ninja.errors.ConfigError: Looks like you created multiple NinjaAPIs or TestClients

_client: TestClient | None = None

def _get_client() -> TestClient:
    global _client
    if _client is None:
        _client = TestClient(main_api)
    return _client


def test_my_endpoint_success():
    client = _get_client()
    resp = client.get("/my-app/my-endpoint", headers=_auth_headers(user))
    assert resp.status_code == 200
    assert resp.json()["info"] == "Success"

def test_my_endpoint_no_auth_401():
    client = _get_client()
    resp = client.get("/my-app/my-endpoint")
    assert resp.status_code == 401
```

## TestClient Singleton Rule

Django Ninja's `TestClient` internally registers URL routes on construction. A second `TestClient(...)` call triggers:

```
ninja.errors.ConfigError: Looks like you created multiple NinjaAPIs or TestClients
```

This is a known framework limitation ([GitHub Issue #229](https://github.com/vitalik/django-ninja/issues/229)). The route registry uses global mutable state that can't be reset.

**Solutions** (pick one):

### A. Module-level lazy singleton (standalone scripts)

```python
_client: TestClient | None = None

def _get_client() -> TestClient:
    global _client
    if _client is None:
        _client = TestClient(main_api)
    return _client
```

### B. pytest session-scoped fixture (pytest projects)

```python
import pytest
from ninja.testing import TestClient
from SheetManage.api import api as main_api

@pytest.fixture(scope="session")
def api_client():
    return TestClient(main_api)

def test_list(api_client):
    resp = api_client.get("/audit/tasks/")
    assert resp.status_code == 200
```

### C. Django TestCase setUpClass (unittest-style)

```python
from django.test import TestCase
from ninja.testing import TestClient
from SheetManage.api import api as main_api

class AuditAPITests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = TestClient(main_api)

    def test_list(self):
        resp = self.client.get("/audit/tasks/")
        assert resp.status_code == 200
```

**Avoid**: Never create `TestClient(router)` in individual test functions or `setUp()`. Never mix creating `TestClient(main_api)` and `TestClient(sub_router)` in the same process.

## Route path conventions

Use `TestClient(main_api)` with **full paths**, not `TestClient(sub_router)` with short paths:

```python
# Prefer: full path on main_api
client = TestClient(main_api)
client.get("/audit/comparison/tasks")       # NOT "/tasks"
client.post("/audit/tasks/{uuid}/apply")    # NOT "/apply"

# Avoid: sub_router with short paths — may cause routing/auth mismatches
client = TestClient(comparison_subrouter)
client.get("/tasks")  # fragile
```

> **Always verify route paths match the API definition.** Mismatches (e.g. `/task` vs `/tasks`) produce `Exception: Cannot resolve "..."` from Ninja's TestClient, which looks like a framework error but is usually a typo in the test.

## Testing authenticated endpoints

```python
import jwt, time
from django.conf import settings

def _make_jwt(user: NocAcc) -> str:
    payload = {
        "acc": user.sps_acc,
        "area": user.area,
        "username": user.username,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600 * 24,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def _auth_headers(user: NocAcc) -> dict[str, str]:
    return {"Authorization": f"Bearer {_make_jwt(user)}"}

def test_auth_endpoint():
    user = _ensure_test_user()
    client = _get_client()
    resp = client.get("/protected/endpoint", headers=_auth_headers(user))
    assert resp.status_code == 200
```

## Testing non-200 status codes

```python
def test_concurrent_409():
    client = _get_client()
    resp = client.post("/audit/comparison/task", ...)
    assert resp.status_code == 409
    assert resp.json().get("error") == "DUPLICATE_TASK"

def test_invalid_token_401():
    client = _get_client()
    resp = client.get("/protected/", headers={"Authorization": "Bearer bad.token"})
    assert resp.status_code == 401
```

## Testing file uploads

```python
from django.core.files.uploadedfile import SimpleUploadedFile

def test_file_upload():
    file = SimpleUploadedFile("test.xlsx", b"...", content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    client = _get_client()
    resp = client.post("/upload", FILES={"files": file}, headers=_auth_headers(user))
    assert resp.status_code == 201
```

## Running tests: always use pytest

```bash
# CORRECT — test isolation, full failure report
python -m pytest tests/sheetScript/test_my_api.py

# WRONG — fragile, misleading output
python tests/sheetScript/test_my_api.py
```

### Why `python test.py` is unreliable

| Problem | Consequence |
|---------|-------------|
| Tests run sequentially in one block | First unhandled exception crashes all remaining tests — later tests never execute |
| No test isolation | State from one test contaminates the next |
| Manual `_assert()` helpers swallow failures | Print "FAIL" but don't propagate, exit code looks successful |
| Piped through `findstr`/`grep` | Exception tracebacks hidden; partial output looks like full success |
| Manual Django setup (`django.setup()`) | Duplicates or conflicts with pytest-django's own setup |

With `python -m pytest`:
- Each test runs independently — one failure never blocks others
- Complete report: `X passed, Y failed` with full tracebacks
- pytest-django handles `DJANGO_SETTINGS_MODULE` and `django.setup()` automatically
- Standard exit codes: non-zero on any failure (CI-friendly)

> **When writing new test files**, use pytest-compatible patterns (plain functions, `pytest` fixtures, `assert` statements). Avoid `if __name__ == "__main__"` dispatch blocks for real test suites — they're only useful for one-off debugging scripts.

## Common pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Running test file directly (`python test.py`) | Looks like tests pass but exceptions are hidden; later tests silently skipped | Always use `python -m pytest` |
| Multiple TestClient instances | `ConfigError: Looks like you created multiple NinjaAPIs or TestClients` | Use singleton/fixture |
| Sub-router paths without prefix | 404 for paths that work in browser | Use `TestClient(main_api)` with full path |
| Missing Content-Type for uploads | 415 Unsupported Media Type | Use `format="multipart"` as kwarg, not header |
| Auth headers not passed | 401 on every request | Verify `Authorization: Bearer <token>` header set |
| Test DB not isolated | Test data leaks between runs | Wrap in `transaction.atomic()` or clean up in `finally` |
| Pytest fixture scope="function" | ConfigError because fixture re-created per test | Use `scope="session"` or `scope="module"` |

---

## Diagnose → Fix → Verify Loop

When the user pastes an error (curl request + stack trace, or a runtime exception), follow this disciplined loop:

```
Reproduce → Minimise → Hypothesise → Instrument → Fix → Regression-test
```

### 1. Reproduce

- Read the exact error trace, note the **file, line, exception type**.
- If the user provides a curl request, attempt to reproduce with the same payload.
- Query Context7 for Django 4.2 and Django Ninja 1.3 documentation before proposing a fix.

### 2. Minimise

- Strip the repro to the smallest failing unit (one endpoint, one query, one schema).
- Check if the error is in **test code** vs **production code** vs **framework**.

### 3. Hypothesise

Match the error against the **Known Error Pattern Database** below. If it matches, explain the root cause and apply the known fix pattern.

### 4. Instrument

- Add targeted logging or `print()` in the failing code path.
- Verify assumptions about data types, query results, and state.

### 5. Fix

- Make the **minimal** change that resolves the error.
- Follow architecture layers (fix in the correct layer: API/Service/Business).
- If the fix changes exception handling, verify the exception handler is registered in `SheetManage/api.py`.

### 6. Regression-test

- Write or update the test that would have caught this bug.
- Run `python -m pytest` on the affected test file.
- Confirm both **success** and **error** paths pass.

---

## Known Error Pattern Database

These are recurring failure modes observed in the `data-support-platform` codebase.

### Pattern 1: `Cannot resolve keyword 'task_uuid'` (Django ORM FK field name mismatch)

**Symptom:**
```
FieldError: Cannot resolve keyword 'task_uuid' into field.
```

**Root cause:** The model defines a `ForeignKey` named `task`, but code tries to filter by `task_uuid`. Django ORM uses the **field name** (`task`), not the database column name (`task_uuid`).

**Fix:**
```python
# WRONG
ComparisonInconsistentRows.objects.filter(task_uuid=uuid)

# CORRECT
ComparisonInconsistentRows.objects.filter(task__uuid=uuid)
```

**Regression test:**
```python
def test_query_by_task_uuid():
    client = _get_client()
    resp = client.get(f"/audit/comparison/tasks/{task.uuid}/inconsistencies")
    assert resp.status_code == 200
```

### Pattern 2: `select_for_update` outside transaction

**Symptom:**
```
TransactionManagementError: select_for_update cannot be used outside of a transaction.
```

**Root cause:** `QuerySet.select_for_update()` requires an active `transaction.atomic()` block.

**Fix:**
```python
from django.db import transaction

def acquire_task(task_id: int):
    with transaction.atomic():
        return AuditTask.objects.select_for_update().get(id=task_id)
```

**Regression test:**
```python
def test_concurrent_task_lock():
    client = _get_client()
    # Verify 409 or proper serialization on concurrent access
```

### Pattern 3: MySQL JSON NaN serialization

**Symptom:**
```
JSON format invalid; NaN is not allowed in JSON
```

**Root cause:** `pandas` DataFrames may contain `NaN`/`Inf`, which MySQL's JSON column rejects.

**Fix:**
```python
import math

def _sanitize_json_value(value):
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value

def df_to_json_safe(df: pd.DataFrame) -> dict:
    return df.applymap(_sanitize_json_value).to_dict(orient="records")
```

**Regression test:**
```python
def test_df_with_nan_serialization():
    df = pd.DataFrame({"a": [1.0, float("nan"), 3.0]})
    result = df_to_json_safe(df)
    assert result[1]["a"] is None
```

### Pattern 4: pydantic V2 `class-based config` deprecation

**Symptom:**
```
PydanticDeprecatedSince20: Support for class-based `config` is deprecated...
```

**Root cause:** pydantic V2 no longer supports `class Config` inside Schema classes.

**Fix:**
```python
# WRONG (pydantic V1 style)
class MyOut(Schema):
    class Config:
        from_attributes = True

# CORRECT (pydantic V2 style)
class MyOut(Schema):
    model_config = {"from_attributes": True}
```

**Regression test:**
```python
def test_schema_no_deprecation():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        MyOut.model_validate({"id": 1})
        assert not any("class-based config" in str(x.message) for x in w)
```

### Pattern 5: `prefetch_related` on non-existent relation

**Symptom:**
```
AttributeError: 'ComparisonInconsistentRows' object has no attribute 'task'
```

**Root cause:** `prefetch_related("task")` was used but the model uses `select_related` (FK) or the related name is different.

**Fix:**
- Use `select_related("task")` for ForeignKey, `prefetch_related("items")` for reverse Many-to-Many/One-to-Many.
- Verify the related name in the model definition.

**Regression test:**
```python
def test_endpoint_with_prefetch():
    client = _get_client()
    resp = client.get("/audit/comparison/tasks/", headers=_auth_headers(user))
    assert resp.status_code == 200
```

---

## Exception Handler Chain Validation

When an error occurs in production but returns **500** instead of the expected status code (e.g., 404 or 422), follow this checklist:

1. **Service layer throws the correct exception?**
   ```python
   # Verify the exception is raised, not swallowed
   raise ItemNotFoundError(f"Item {item_id} not found") from e
   ```

2. **Exception registered in `SheetManage/api.py`?**
   ```python
   @api.exception_handler(ItemNotFoundError)
   def handle_item_not_found(request, exc):
       return api.create_response(request, {"detail": str(exc)}, status=404)
   ```

3. **Test verifies the correct status code?**
   ```python
   def test_not_found_returns_404():
       client = _get_client()
       resp = client.get("/items/99999")
       assert resp.status_code == 404  # NOT 500
   ```

4. **No generic `except Exception` swallowing the custom exception?**
   ```python
   # WRONG — swallows custom exceptions, causing 500
   try:
       return service.get_item(item_id)
   except Exception:
       logger.error(...)
       raise  # re-raise is OK, but bare `except Exception` is risky
   ```

---

## Brownfield Test Coverage Audit

When the user says "检查...的测试覆盖率" or "添加...接口的API层集成测试", follow this workflow:

### Step 1: Scan

Read the target module(s) and identify:
- All public API endpoints (router operations)
- All public service methods
- All exception paths (custom exceptions)

### Step 2: Matrix

Produce a coverage matrix:

| Endpoint/Method | Has Test? | Test Type | Gaps |
|-----------------|-----------|-----------|------|
| `GET /tasks/` | ❌ | — | success + auth + pagination |
| `POST /tasks/` | ✅ | API integration | missing 409 duplicate |
| `AuditService.import_excel()` | ❌ | — | success + NaN data + bad file |

### Step 3: Prioritize

Label each gap:
- **P0** (must have): Happy path + critical error paths (auth, 404, 409)
- **P1** (should have): Edge cases (empty input, pagination limits)
- **P2** (nice to have): Rare error conditions, concurrent access

### Step 4: Implement

Generate tests following the patterns below. Reference `tests/sheetScript/test_check_lans.py` for style.

### Step 5: Verify

Run `python -m pytest` and confirm all new tests pass.

---

## Test Structure & Requirements

### Structure (Arrange-Act-Assert)

```python
# Example test structure based on existing patterns
import pytest
from django.test import TestCase
from sheetScript.services.item_service import ItemService, ItemNotFoundError

class TestItemService(TestCase):
    def setUp(self):
        self.service = ItemService()
        # Setup test data
        
    def test_get_item_success(self):
        """Test successful item retrieval."""
        # Arrange
        item = Item.objects.create(name="Test Item")
        
        # Act
        result = self.service.get_item(item.id)
        
        # Assert
        self.assertEqual(result.id, item.id)
        self.assertEqual(result.name, "Test Item")
        
    def test_get_item_not_found(self):
        """Test item not found raises exception."""
        # Act & Assert
        with self.assertRaises(ItemNotFoundError):
            self.service.get_item(999)  # Non-existent ID
            
    def test_create_item_with_valid_data(self):
        """Test item creation with valid data."""
        # Act
        item_id = self.service.create_item(name="New Item", category="Test")
        
        # Assert
        self.assertIsInstance(item_id, int)
        self.assertTrue(Item.objects.filter(id=item_id).exists())
```

### Requirements

1. **Service layer**: Write unit tests for all service methods
2. **API endpoints**: Write integration tests for critical endpoints
3. **Error cases**: Test both success and error scenarios
4. **Authentication**: Test permission and authentication when applicable
5. **Data validation**: Test input validation and error handling

### Scenario: Testing a new service method

1. Reference `test_check_lans.py` patterns
2. Test success cases with valid data
3. Test error cases with invalid data
4. Test exception propagation
5. Mock external dependencies when needed
