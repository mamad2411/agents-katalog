---
applyTo: "**/*.{test,spec}.{ts,tsx,js,jsx,py}"
---

# Testing Standards

## General Principles

- Tests document behavior — write them as specifications, not implementation mirrors
- Each test should be independent — no shared mutable state between tests
- Use descriptive test names: `test_user_creation_fails_with_duplicate_email`
- Follow Arrange-Act-Assert (AAA) pattern in every test
- Aim for 80%+ coverage on business logic; 100% on security-critical paths
- Test edge cases: empty inputs, nulls, boundary values, error conditions

## Python Backend Testing (pytest + pytest-asyncio)

### Structure
```python
"""Tests for user service."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Create async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestUserCreation:
    """Test suite for user creation endpoint."""

    async def test_creates_user_with_valid_data(self, client: AsyncClient) -> None:
        response = await client.post("/api/v1/users", json={...})
        assert response.status_code == 201

    async def test_rejects_duplicate_email(self, client: AsyncClient) -> None:
        ...
```

### Rules
- Use `pytest.mark.asyncio` or configure `asyncio_mode = "auto"` globally
- Fixtures in `conftest.py`, scoped appropriately (`function`, `class`, `session`)
- Use `httpx.AsyncClient` with `ASGITransport` for API tests — not `TestClient`
- Factory fixtures for test data: `user_factory`, `project_factory`
- Database tests use transactions that roll back — never persist test data
- Mock external services with `pytest-mock` or `respx` for HTTP
- Parametrize repetitive cases with `@pytest.mark.parametrize`

## Frontend Testing (Vitest + Testing Library)

### Structure
```typescript
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/vue' // or @testing-library/react
import userEvent from '@testing-library/user-event'
import MyComponent from './MyComponent.vue'

describe('MyComponent', () => {
  it('renders greeting when name is provided', () => {
    render(MyComponent, { props: { name: 'Alice' } })
    expect(screen.getByText('Hello, Alice')).toBeInTheDocument()
  })

  it('emits submit event with form data', async () => {
    const user = userEvent.setup()
    const { emitted } = render(MyComponent)
    await user.type(screen.getByLabelText('Email'), 'test@example.com')
    await user.click(screen.getByRole('button', { name: 'Submit' }))
    expect(emitted().submit[0]).toEqual([{ email: 'test@example.com' }])
  })
})
```

### Rules
- Query by accessibility role first: `getByRole`, `getByLabelText`, `getByText`
- Use `getByTestId` only as last resort
- Use `userEvent` over `fireEvent` for realistic interaction simulation
- Mock API calls with `msw` (Mock Service Worker) at the network layer
- Test component behavior, not internal state or implementation details
- Snapshot tests only for stable, design-system components — not business logic
- Test composables/hooks in isolation with `renderHook()`

## What to Test

| Layer | What to Test | What NOT to Test |
|-------|-------------|------------------|
| API routes | Status codes, response shape, auth, validation errors | Framework internals |
| Services | Business rules, edge cases, error handling | Database queries directly |
| Repositories | Query correctness, pagination, filtering | ORM internals |
| Components | User interactions, conditional rendering, events | CSS styles, third-party libs |
| Composables | Reactive behavior, side effects, cleanup | Vue/React internals |
| Stores | Actions, getters, state transitions | Store library internals |
