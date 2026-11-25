---
name: tdd-workflow
description: Use this skill when creating new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.
---

# Test-Driven Development Workflow

This skill ensures all code development follows TDD principles with comprehensive test coverage.

## When to Activate

- Creating new features or capabilities
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new components

## Core Principles

### 1. Tests Before Code
Always write tests first, then implement code to pass those tests.

### 2. Coverage Requirements
- Minimum 80% coverage (unit + integration + E2E)
- Cover all edge cases
- Test error scenarios
- Validate boundary conditions

### 3. Test Types

#### Unit Tests
- Individual functions and utilities
- Component logic
- Pure functions
- Helpers and utilities

#### Integration Tests
- API endpoints
- Database operations
- Service-to-service interactions
- External API calls

#### E2E Tests
- Critical user flows
- Complete workflows
- Browser automation
- UI interactions

## TDD Workflow Steps

### Step 1: Write the User Story
```
As a [role], I want to [action], so that [benefit].

Example:
As a user, I want to track my asset values daily,
so that I can see my portfolio performance over time.
```

### Step 2: Generate Test Cases

```go
func TestAssetService_CalculateDailyValue(t *testing.T) {
    tests := []struct {
        name    string
        assets  []Asset
        want    float64
        wantErr bool
    }{
        {
            name:   "single asset",
            assets: []Asset{{Quantity: 10, Price: 100}},
            want:   1000,
        },
        {
            name:   "multiple assets",
            assets: []Asset{{Quantity: 10, Price: 100}, {Quantity: 5, Price: 200}},
            want:   2000,
        },
        {
            name:    "empty portfolio",
            assets:  []Asset{},
            want:    0,
            wantErr: false,
        },
        {
            name:    "negative quantity",
            assets:  []Asset{{Quantity: -1, Price: 100}},
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := CalculateDailyValue(tt.assets)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Step 3: Run Tests (Should FAIL)
```bash
go test ./...
# Tests should fail — nothing is implemented yet
```

### Step 4: Implement the Code
Write the minimum code to make the tests pass:

```go
func CalculateDailyValue(assets []Asset) (float64, error) {
    var total float64
    for _, asset := range assets {
        if asset.Quantity < 0 {
            return 0, errors.New("negative quantity not allowed")
        }
        total += asset.Quantity * asset.Price
    }
    return total, nil
}
```

### Step 5: Run Tests (Should PASS)
```bash
go test ./...
# All tests should pass now
```

### Step 6: Refactor
Improve code quality while keeping tests green:
- Remove duplication
- Improve naming
- Optimize performance
- Improve readability

### Step 7: Check Coverage
```bash
# Go
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# TypeScript/React
npm run test -- --coverage
```

## Test Patterns

### Go Unit Test Pattern
```go
func TestHandler_CreateAsset(t *testing.T) {
    // Arrange
    mockService := &MockAssetService{
        createFn: func(ctx context.Context, req *CreateAssetRequest) (*Asset, error) {
            return &Asset{ID: 1, Name: req.Name}, nil
        },
    }
    handler := NewAssetHandler(mockService)

    body := `{"name":"Bitcoin","ticker":"BTC","quantity":0.5,"price":50000}`
    req := httptest.NewRequest("POST", "/api/assets", strings.NewReader(body))
    req.Header.Set("Content-Type", "application/json")
    rec := httptest.NewRecorder()

    // Act
    router := gin.New()
    router.POST("/api/assets", handler.Create)
    router.ServeHTTP(rec, req)

    // Assert
    if rec.Code != http.StatusCreated {
        t.Errorf("got status %d, want %d", rec.Code, http.StatusCreated)
    }
}
```

### React Component Test Pattern (Vitest)
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { AssetCard } from './AssetCard'

describe('AssetCard', () => {
  const mockAsset = {
    id: '1',
    name: 'Bitcoin',
    ticker: 'BTC',
    value: 50000,
  }

  it('renders asset information', () => {
    render(<AssetCard asset={mockAsset} />)
    expect(screen.getByText('Bitcoin')).toBeInTheDocument()
    expect(screen.getByText('BTC')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn()
    render(<AssetCard asset={mockAsset} onClick={handleClick} />)
    fireEvent.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

## Common Testing Mistakes to Avoid

### ❌ Testing implementation details
```go
// Don't test private fields directly
```

### ✅ Test observable behavior
```go
// Test the public API and its results
```

### ❌ Fragile selectors
```typescript
await page.click('.css-class-xyz')  // Breaks easily
```

### ✅ Semantic selectors
```typescript
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

### ❌ Tests depending on each other
```go
// test1 creates data that test2 depends on
```

### ✅ Independent tests
```go
// Each test sets up its own data in setup/teardown
```

## Best Practices

1. **Write tests first** — Always follow TDD
2. **One assert per test** — Focus on a single behavior
3. **Descriptive test names** — Explain what is tested
4. **Arrange-Act-Assert** — Clear test structure
5. **Mock external dependencies** — Isolate unit tests
6. **Test edge cases** — null, undefined, empty, extreme values
7. **Test error paths** — Not just the happy path
8. **Keep tests fast** — Unit tests under 50ms each
9. **Clean up after tests** — No side effects
10. **Review coverage reports** — Identify gaps

---

**Remember**: Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability.
