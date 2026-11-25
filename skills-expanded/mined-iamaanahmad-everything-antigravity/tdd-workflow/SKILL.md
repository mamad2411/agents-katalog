---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.
model: gemini-2.0-pro-exp
---

# Test-Driven Development Workflow

This skill ensures all code development follows TDD principles with comprehensive test coverage in Antigravity projects.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new components

## Core Principles

1. **Tests BEFORE Code** - Always write tests first
2. **80%+ Coverage** - Unit + integration + E2E
3. **All edge cases covered** - Null, empty, boundary, error scenarios

## TDD Workflow Steps

### Step 1: Write User Journeys
```
As a [role], I want to [action], so that [benefit]
```

### Step 2: Generate Test Cases

```typescript
describe('Feature', () => {
  it('returns expected result for valid input', async () => { /* ... */ })
  it('handles empty input gracefully', async () => { /* ... */ })
  it('falls back correctly when dependency unavailable', async () => { /* ... */ })
  it('sorts results correctly', async () => { /* ... */ })
})
```

### Step 3: Run Tests (They Should Fail)
```bash
npm test
# Tests should fail - implementation doesn't exist yet
```

### Step 4: Implement Minimal Code
Write just enough to make tests pass.

### Step 5: Run Tests Again
```bash
npm test
# Tests should now pass
```

### Step 6: Refactor
Improve code quality while keeping tests green.

### Step 7: Verify Coverage
```bash
npm run test:coverage
# Verify 80%+ coverage achieved
```

## Testing Patterns

### Unit Test Pattern (Jest/Vitest)

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click</Button>)
    fireEvent.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### API Integration Test Pattern

```typescript
describe('GET /api/resources', () => {
  it('returns resources successfully', async () => {
    const request = new NextRequest('http://localhost/api/resources')
    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.success).toBe(true)
    expect(Array.isArray(data.data)).toBe(true)
  })

  it('validates query parameters', async () => {
    const request = new NextRequest('http://localhost/api/resources?limit=invalid')
    const response = await GET(request)
    expect(response.status).toBe(400)
  })
})
```

### E2E Test Pattern (Playwright)

```typescript
import { test, expect } from '@playwright/test'

test('user can search and view results', async ({ page }) => {
  await page.goto('/')
  await page.fill('input[placeholder="Search"]', 'query')
  await page.waitForTimeout(600) // debounce

  const results = page.locator('[data-testid="result-card"]')
  await expect(results).toHaveCount(5, { timeout: 5000 })
})
```

## Test File Organization

```
src/
├── components/
│   └── Button/
│       ├── Button.tsx
│       └── Button.test.tsx
├── app/api/
│   └── resources/
│       ├── route.ts
│       └── route.test.ts
└── e2e/
    └── flows.spec.ts
```

## Mocking External Services

```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => Promise.resolve({ data: [{ id: 1, name: 'Test' }], error: null }))
    }))
  }
}))
```

## Coverage Thresholds

```json
{
  "jest": {
    "coverageThresholds": {
      "global": { "branches": 80, "functions": 80, "lines": 80, "statements": 80 }
    }
  }
}
```

## Common Mistakes to Avoid

```typescript
// ❌ Testing implementation details
expect(component.state.count).toBe(5)

// ✅ Test user-visible behavior
expect(screen.getByText('Count: 5')).toBeInTheDocument()

// ❌ Brittle selectors
await page.click('.css-class-xyz')

// ✅ Semantic selectors
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

**Remember**: Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability.
