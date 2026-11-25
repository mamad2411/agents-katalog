---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.
origin: AI Dev Kit
disable-model-invocation: false
---

# Test-Driven Development Workflow

This skill ensures all code development follows TDD principles with comprehensive test coverage.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new components
- Modifying existing test targets

## Core Principles

### 1. Tests BEFORE Code

ALWAYS write tests first, then implement code to make tests pass. No exceptions for production code.

### 2. Coverage Requirements

- **Minimum 80% line coverage** (unit + integration + E2E)
- **Minimum 70% branch coverage**
- All edge cases covered (null, empty, boundary, concurrent)
- Error scenarios tested (timeouts, network failures, invalid input)
- Boundary conditions verified

### 3. Test Types

#### Unit Tests
- Individual functions and utilities
- Pure functions with no side effects
- Component logic
- Helpers and utilities
- Fast execution (<50ms each)

#### Integration Tests
- API endpoints (FastAPI routes, Express handlers)
- Database operations (SQLAlchemy, Prisma)
- Service interactions
- External API calls (with mocked responses)

#### E2E Tests (Playwright)
- Critical user flows
- Complete workflows
- Browser automation
- UI interactions and state transitions

### 4. Git Checkpoints

If the repository is under Git, create a checkpoint commit after each TDD stage:

- **RED checkpoint**: `test: add failing test for <feature or bug>`
- **GREEN checkpoint**: `fix: <feature or bug> — make tests pass`
- **REFACTOR checkpoint**: `refactor: clean up after <feature> implementation`

Do not squash or rewrite these commits until the workflow is complete. Each checkpoint must be reachable from HEAD.

---

## TDD Workflow Steps

### Step 1: Write User Journeys

Define the behavior from the user's perspective:

```
As a [role], I want to [action], so that [benefit]

Example:
As a developer, I want to validate user input at the API boundary,
so that invalid requests are rejected with clear error messages.
```

### Step 2: Generate Test Cases

For each user journey, create comprehensive test cases:

**Python (pytest):**
```python
import pytest
from fastapi.testclient import TestClient
from app.api.users import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
client = TestClient(app)

class TestCreateUser:
    def test_creates_user_with_valid_input(self):
        """User is created and returned with generated ID."""
        response = client.post("/users", json={
            "name": "Alice",
            "email": "alice@example.com"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"

    def test_rejects_missing_name(self):
        """Returns 422 when name is missing."""
        response = client.post("/users", json={"email": "alice@example.com"})
        assert response.status_code == 422

    def test_rejects_invalid_email(self):
        """Returns 422 when email format is invalid."""
        response = client.post("/users", json={"name": "Alice", "email": "not-an-email"})
        assert response.status_code == 422

    def test_rejects_duplicate_email(self):
        """Returns 409 when email already exists."""
        client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
        response = client.post("/users", json={"name": "Alice 2", "email": "alice@example.com"})
        assert response.status_code == 409
```

**TypeScript (Vitest):**
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createUser } from './users'
import { db } from '../db'

vi.mock('../db')

describe('createUser', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('creates user with valid input', async () => {
    vi.mocked(db.user.create).mockResolvedValue({
      id: 'usr_123',
      name: 'Alice',
      email: 'alice@example.com'
    })

    const result = await createUser({
      name: 'Alice',
      email: 'alice@example.com'
    })

    expect(result.id).toBe('usr_123')
    expect(db.user.create).toHaveBeenCalledWith({
      data: { name: 'Alice', email: 'alice@example.com' }
    })
  })

  it('throws when email is missing', async () => {
    await expect(
      createUser({ name: 'Alice', email: '' })
    ).rejects.toThrow('Email is required')
  })

  it('throws on duplicate email', async () => {
    vi.mocked(db.user.create).mockRejectedValue(
      new Error('Unique constraint failed on email')
    )

    await expect(
      createUser({ name: 'Alice', email: 'alice@example.com' })
    ).rejects.toThrow('Email already exists')
  })
})
```

### Step 3: Run Tests — Must Fail (RED Gate)

```bash
# Python
pytest tests/test_users.py -v
# Tests should FAIL — we haven't implemented yet

# TypeScript
npx vitest run tests/users.test.ts
# Tests should FAIL — we haven't implemented yet
```

**This step is mandatory.** Before modifying production code, verify a valid RED state:

- **Runtime RED**: The test compiles, executes, and fails for the intended business-logic reason
- **Compile-time RED**: The test references missing types/functions and the compile failure is the intended signal

A test that was only written but not compiled/executed does **not** count as RED.

### Step 4: Implement Minimal Code

Write the minimum code to make tests pass:

**Python:**
```python
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/users", tags=["users"])

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate):
    # Minimal implementation — just make tests pass
    return UserResponse(id="usr_new", name=user.name, email=user.email)
```

**TypeScript:**
```typescript
import { db } from '../db'

interface UserInput {
  name: string
  email: string
}

interface User {
  id: string
  name: string
  email: string
}

export async function createUser(input: UserInput): Promise<User> {
  if (!input.email) {
    throw new Error('Email is required')
  }

  try {
    return await db.user.create({
      data: { name: input.name, email: input.email }
    })
  } catch (error: unknown) {
    if (error instanceof Error && error.message.includes('Unique constraint')) {
      throw new Error('Email already exists')
    }
    throw error
  }
}
```

### Step 5: Run Tests Again — Must Pass (GREEN)

```bash
# Python
pytest tests/test_users.py -v
# All tests should PASS now

# TypeScript
npx vitest run tests/users.test.ts
# All tests should PASS now
```

Rerun the same test target and confirm the previously failing tests are now GREEN. Only then proceed to refactor.

### Step 6: Refactor

Improve code quality while keeping tests green:

- Remove duplication
- Improve naming
- Extract shared utilities
- Add dependency injection where needed
- Optimize performance if needed
- Enhance readability

```bash
# Verify tests still pass after each refactor
pytest tests/test_users.py -v
npx vitest run tests/users.test.ts
```

### Step 7: Verify Coverage

```bash
# Python
pytest --cov=app --cov-report=term-missing --cov-report=html

# TypeScript
npx vitest run --coverage
```

Verify 80%+ line coverage and 70%+ branch coverage. Identify and fill gaps.

---

## Testing Patterns

### Python Unit Test (pytest)

```python
import pytest
from datetime import datetime

def calculate_discount(price: float, discount_pct: float) -> float:
    if discount_pct < 0 or discount_pct > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_pct / 100)

class TestCalculateDiscount:
    def test_no_discount(self):
        assert calculate_discount(100.0, 0) == 100.0

    def test_full_discount(self):
        assert calculate_discount(100.0, 100) == 0.0

    def test_partial_discount(self):
        assert calculate_discount(100.0, 25) == 75.0

    def test_rejects_negative_discount(self):
        with pytest.raises(ValueError, match="between 0 and 100"):
            calculate_discount(100.0, -10)

    def test_rejects_excessive_discount(self):
        with pytest.raises(ValueError, match="between 0 and 100"):
            calculate_discount(100.0, 110)
```

### FastAPI Integration Test

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

def test_get_user_not_found(client: TestClient):
    """Returns 404 when user does not exist."""
    with patch("app.api.users.db") as mock_db:
        mock_db.user.get.return_value = None
        response = client.get("/users/nonexistent")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
```

### TypeScript React Component Test

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { UserCard } from './UserCard'

describe('UserCard', () => {
  const mockUser = { id: '1', name: 'Alice', email: 'alice@example.com' }

  it('renders user information', () => {
    render(<UserCard user={mockUser} onSelect={() => {}} />)
    expect(screen.getByText('Alice')).toBeInTheDocument()
    expect(screen.getByText('alice@example.com')).toBeInTheDocument()
  })

  it('calls onSelect when clicked', () => {
    const handleSelect = vi.fn()
    render(<UserCard user={mockUser} onSelect={handleSelect} />)
    fireEvent.click(screen.getByRole('button'))
    expect(handleSelect).toHaveBeenCalledWith('1')
  })
})
```

### E2E Test (Playwright)

```typescript
import { test, expect } from '@playwright/test'

test('user can create account and log in', async ({ page }) => {
  // Navigate to signup
  await page.goto('/signup')

  // Fill form
  await page.fill('input[name="name"]', 'Alice')
  await page.fill('input[name="email"]', 'alice@example.com')
  await page.fill('input[name="password"]', 'securepass123')

  // Submit
  await page.click('button[type="submit"]')

  // Verify redirect to dashboard
  await expect(page).toHaveURL(/\/dashboard/)
  await expect(page.locator('h1')).toContainText('Welcome, Alice')
})
```

---

## Mocking External Services

### Python: Mock Database

```python
from unittest.mock import MagicMock, patch

@patch("app.db.session")
def test_user_query(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = {
        "id": "1", "name": "Alice"
    }
    result = get_user("1")
    assert result["name"] == "Alice"
```

### TypeScript: Mock API

```typescript
vi.mock('@/lib/api', () => ({
  fetchUser: vi.fn(() => Promise.resolve({ id: '1', name: 'Alice' }))
}))
```

---

## Test File Organization

```
project/
├── src/
│   ├── api/
│   │   ├── users.py              # FastAPI routes
│   │   └── users.test.py         # Integration tests
│   ├── models/
│   │   ├── user.py               # SQLAlchemy models
│   │   └── user.test.py          # Unit tests
│   └── services/
│       ├── user_service.py       # Business logic
│       └── user_service.test.py  # Unit tests
├── tests/
│   ├── e2e/
│   │   ├── test_auth.spec.ts     # Playwright E2E
│   │   └── test_crud.spec.ts
│   └── conftest.py               # Shared fixtures
```

---

## Common Mistakes to Avoid

| Mistake | Why It's Wrong | Correct Approach |
|---|---|---|
| Testing implementation details | Breaks on refactor | Test user-visible behavior |
| Brittle selectors (`.css-abc123`) | Breaks on CSS changes | Use semantic selectors (`[data-testid="..."]`) |
| Tests depending on each other | Order-dependent, flaky | Each test sets up its own data |
| `any` types in TypeScript tests | No type safety | Use proper interfaces |
| Skipping error paths | Only happy path covered | Test null, empty, timeout, 500 |
| `console.log` in test output | Noise, not assertions | Use proper assertions |

---

## Best Practices

1. **Write Tests First** — Always TDD, no exceptions
2. **One Behavior Per Test** — Focus on single assertion
3. **Descriptive Names** — `test_rejects_missing_email` not `test1`
4. **Arrange-Act-Assert** — Clear structure in every test
5. **Mock External Dependencies** — Isolate the unit under test
6. **Test Edge Cases** — Null, empty, boundary, concurrent
7. **Test Error Paths** — Not just the happy path
8. **Keep Tests Fast** — Unit tests under 50ms each
9. **Clean Up After Tests** — No side effects between tests
10. **Review Coverage Reports** — Identify and fill gaps

## Success Metrics

- [ ] 80%+ line coverage achieved
- [ ] 70%+ branch coverage achieved
- [ ] All tests passing (green)
- [ ] No skipped or disabled tests
- [ ] Fast test execution (< 30s for unit suite)
- [ ] E2E tests cover critical user flows
- [ ] Tests catch bugs before production

---

**Remember:** Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability.
