---
name: "test-and-verify"
description: "Write tests and verify implementation works"
---

# Test and Verify Skill

Write tests in the same context as implementation to catch bugs early.

## Trigger Phrases
- "write tests"
- "add tests for this"
- "test this feature"
- "verify this works"

## Why Same Context?

Testing in the same context where you implemented:
- Model has full context of implementation details
- Almost always finds edge cases/bugs
- More relevant test cases
- Catches mistakes immediately

## Workflow

### 1. Identify What to Test

**Do write tests for**:
- Business logic
- API endpoints
- Data transformations
- Edge cases
- Error handling
- Complex components

**Skip tests for**:
- Pure UI styling tweaks
- Trivial getters/setters
- Configuration files
- One-off scripts

### 2. Test Structure

#### Unit Tests
Test individual functions/components in isolation.

```typescript
// Example: Function testing
describe('calculateDiscount', () => {
  it('applies 10% discount for regular users', () => {
    expect(calculateDiscount(100, 'regular')).toBe(90);
  });

  it('applies 20% discount for premium users', () => {
    expect(calculateDiscount(100, 'premium')).toBe(80);
  });

  it('handles edge case of zero amount', () => {
    expect(calculateDiscount(0, 'regular')).toBe(0);
  });
});
```

#### Integration Tests  
Test how parts work together.

```typescript
// Example: API endpoint
describe('POST /api/users', () => {
  it('creates user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'test@example.com' });
    
    expect(response.status).toBe(201);
    expect(response.body.name).toBe('Test');
  });

  it('rejects invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'invalid' });
    
    expect(response.status).toBe(400);
  });
});
```

#### Component Tests (React)
```typescript
describe('LoginButton', () => {
  it('renders with correct text', () => {
    render(<LoginButton />);
    expect(screen.getByText('Login')).toBeInTheDocument();
  });

  it('calls onLogin when clicked', () => {
    const onLogin = jest.fn();
    render(<LoginButton onLogin={onLogin} />);
    
    fireEvent.click(screen.getByText('Login'));
    expect(onLogin).toHaveBeenCalledTimes(1);
  });
});
```

### 3. Run Tests
```bash
# TypeScript/JavaScript
npm test
npm run test:watch  # Watch mode during development

# Go
go test ./...
go test -v ./... # Verbose

# Python  
pytest
pytest -v  # Verbose
```

### 4. Fix Issues Found

When tests fail:
1. Read error message carefully
2. Check if test is wrong or implementation is wrong
3. Fix the actual bug
4. Re-run tests
5. Repeat until green

### 5. Update Tests When Code Changes

Tests should evolve with code:
- Update when behavior changes intentionally
- Remove tests for deleted features
- Add tests for new edge cases discovered

## Test Coverage Goals

Don't aim for 100% coverage. Aim for:
- ✅ All critical paths tested
- ✅ Edge cases covered
- ✅ Error handling verified
- ✅ Complex logic has tests
- ❌ Don't test framework code
- ❌ Don't test trivial code

## Common Patterns

### Test Error Handling
```typescript
it('handles network error gracefully', async () => {
  // Mock network failure
  jest.spyOn(global, 'fetch').mockRejectedValue(new Error('Network error'));
  
  const result = await fetchUser(1);
  expect(result.error).toBe('Network error');
});
```

### Test Async Code
```typescript
it('waits for async operation', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});
```

### Test State Changes (React)
```typescript
it('toggles state on click', () => {
  render(<Toggle />);
  const button = screen.getByRole('button');
  
  expect(button).toHaveAttribute('aria-pressed', 'false');
  fireEvent.click(button);
  expect(button).toHaveAttribute('aria-pressed', 'true');
});
```

## Verification Checklist

After writing tests:
- [ ] All tests pass
- [ ] Tests cover happy path
- [ ] Tests cover edge cases
- [ ] Tests cover error scenarios  
- [ ] Test names are clear
- [ ] Tests are fast (< 1s each for unit tests)
- [ ] No flaky tests (run multiple times to verify)

## Integration with Development

### During Feature Development
1. Implement feature
2. Write tests in same session
3. Run tests
4. Fix bugs found
5. Commit both code and tests together

### During Bug Fixes
1. Write failing test that reproduces bug
2. Fix the bug
3. Verify test now passes
4. Commit fix with test (regression test)

## Anti-Patterns

❌ **Don't**: Write tests after forgetting implementation details
✅ **Do**: Write tests immediately while context is fresh

❌ **Don't**: Test implementation details
✅ **Do**: Test behavior and outcomes

❌ **Don't**: Write flaky tests that sometimes fail
✅ **Do**: Write deterministic tests

❌ **Don't**: Make tests depend on each other
✅ **Do**: Keep tests independent

---

**Remember**: Tests written in the same context as implementation almost always find bugs. Don't skip this step.
