---
name: testing-pytest
description: "Apply when writing tests with pytest, designing test suites, or fixing flaky tests. Covers: fixtures, async tests, mocking, parametrize, coverage strategy, integration vs unit. Trigger for: test, pytest, unittest, mock, coverage, TDD."
---

# TESTING PYTEST — Production Test Patterns

## Test Architecture
```
tests/
├── unit/          # fast, no I/O, mock everything external
├── integration/   # real DB (test container), real Redis
├── e2e/           # real HTTP calls, staging env
└── conftest.py    # shared fixtures
```
**Coverage target: 80% minimum. 100% is not the goal — test behavior, not implementation.**

## Fixtures — The right way
```python
# conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest_asyncio.fixture(scope="session")
async def engine():
    """One engine per test session (fast)."""
    eng = create_async_engine("postgresql+asyncpg://test:test@localhost/testdb")
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()

@pytest_asyncio.fixture(autouse=True)
async def rollback(engine):
    """Each test gets a clean transaction, rolled back after."""
    async with engine.begin() as conn:
        await conn.begin_nested()
        yield
        await conn.rollback()

@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
```

## Parametrize — Test multiple cases without duplication
```python
@pytest.mark.parametrize("status,expected_code", [
    ("pending", 200),
    ("running", 200),
    ("invalid_status", 422),
    ("", 422),
])
async def test_job_filter(client, status, expected_code):
    resp = await client.get(f"/jobs?status={status}")
    assert resp.status_code == expected_code
```

## Mocking — Mock at the boundary
```python
from unittest.mock import AsyncMock, patch

async def test_job_submission_sends_notification():
    with patch("app.services.notify.send_email", new_callable=AsyncMock) as mock_email:
        result = await submit_job(task="build", notify=True)
        mock_email.assert_called_once_with(
            to="user@example.com",
            subject=f"Job {result.id} submitted"
        )
```

## Async Tests
```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # no need for @pytest.mark.asyncio on every test

# All async test functions work automatically
async def test_something():
    result = await some_async_function()
    assert result is not None
```

## What to test
```python
# ✅ Test behavior, not implementation
async def test_failed_job_goes_to_dlq():
    """When a job fails 3 times, it must appear in the DLQ."""
    job = await submit_job(payload={"will_fail": True})
    await process_with_retries(job, max_retries=3)
    dlq = await get_dlq_jobs()
    assert any(j.id == job.id for j in dlq)

# ❌ Don't test internals
def test_retry_counter_increments():  # implementation detail
    ...
```

## Forbidden
❌ `time.sleep()` in tests — use `freezegun` or mock
❌ Tests that depend on execution order
❌ Shared mutable state between tests (use fixtures)
❌ Testing private methods (`_method`)
❌ `assert response.status_code == 200` without checking body
❌ Database tests without rollback/cleanup
