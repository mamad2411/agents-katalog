---
name: write-pytest-service-tests
description: >-
  Load this skill when writing pytest tests for a Python service: unit and integration tests,
  fixtures, and what to mock versus run against a real dependency. Auto-load when a test file is
  created or modified.
disable-model-invocation: false
user-invocable: false
paths:
  - "**/test_*.py"
  - "**/*_test.py"
  - "**/tests/**"
  - "**/conftest.py"
compatibility: >-
  Requires Python 3.12+ and the `uv` package manager on PATH, plus network access to PyPI on first
  sync; `pytest`, `pytest-asyncio`, and `httpx` come from `uv sync`, not from a global install.
  Database-backed tests additionally need a reachable PostgreSQL instance dedicated to tests - an
  in-memory substitute will not do.
license: Apache-2.0
---

# Write pytest Tests for a Service

Framework: **pytest** with **pytest-asyncio** (`asyncio_mode = "auto"` in `pyproject.toml`)

HTTP testing: `httpx.AsyncClient` (async, preferred) or FastAPI `TestClient` (sync)

Write service tests at the lowest tier that can show the behavior, with real PostgreSQL and mocked
external APIs. Done when each test asserts one behavior and the suite leaves no database state behind.

## Procedure

1. Choose the inputs and scenarios first (see Hands off to).
2. Put each test in `tests/unit/`, `tests/integration/`, or `tests/system/` by what it needs.
3. Mock external APIs only. Never mock PostgreSQL in an integration test.
4. Roll back every database write after the test.
5. Run coverage and read the untested regions. Never add a test just to reach the floor.

## Rules

### Test structure

```
backend/
└── tests/
    ├── unit/         # Isolated — no I/O, mock all external dependencies
    ├── integration/  # Real database, mock only external APIs (LLM, payment)
    ├── system/       # Full-stack E2E — real infra, real HTTP
    └── conftest.py   # Shared fixtures: test DB, async client, mock factories
```

Test files mirror source structure. Naming: `test_<what>_<expected_behavior>.py`. One logical behavior per test.

### Unit tests: no I/O

```python
class TestOrderService:
    async def test_reserve_rejects_qty_above_stock(self):
        service = OrderService(stock={"A-1": 1})
        result = await service.reserve("A-1", qty=2)
        assert result.is_invalid
        assert "insufficient stock" in result.reason
```

### Integration tests: real database, never mocked

```python
class TestOrdersAPI:
    async def test_post_order_persists_row(self, async_client: AsyncClient, test_db):
        response = await async_client.post("/orders", json={"sku": "A-1", "qty": 2})
        assert response.status_code == 201
        order_id = response.json()["order_id"]
        row = await test_db.fetchrow(
            "SELECT * FROM orders WHERE order_id = $1", order_id
        )
        assert row is not None
```

Each test that writes data must run in a transaction that rolls back after the test.

### Mocking rules

- Mock external HTTP services
- Do **not** mock PostgreSQL in integration tests: a mock cannot catch bad SQL, a constraint
  violation, or migration drift, which are this tier's main risks
- Use `unittest.mock` or `pytest-mock`

### Coverage floor

A floor for finding blind spots, not a goal. Below the number, look for the untested regions.
Reaching it proves nothing and is never a reason to add tests.

| Area                                  | Floor |
| ------------------------------------- | ----- |
| Python application package            | 80%   |
| Core business logic / domain services | 95%   |

```bash
uv run pytest --cov=app --cov-report=term-missing
```

## Hands off to

This skill covers the **tooling** — runner, fixtures, mocking, coverage. It does not decide
_which_ inputs and cases a test should cover. Before writing the cases:

- Invoke the Skill tool with skill="ceh-testing:design-test-cases" to choose them. It supplies
  equivalence partitions, boundary values, decision tables, pairwise combinations, properties, and
  metamorphic relations — stack-agnostic technique that the sections above assume has already been
  applied.
