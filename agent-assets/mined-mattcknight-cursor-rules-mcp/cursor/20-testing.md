---
description: Testing standards and best practices
globs: ["**/*test*", "**/*spec*"]
alwaysApply: false
---

# Testing Guidelines

## 🔴 MANDATORY Coverage Requirements

**Minimum Coverage Standards:**
- **Unit Tests:** 90%+ coverage (MANDATORY)
- **Integration Tests:** 85%+ coverage (MANDATORY)
- **E2E Tests:** All critical user flows (MANDATORY)

**Zero Tolerance Rules:**
- ❌ **NEVER skip unit tests** - They are MANDATORY, not optional
- ❌ **NEVER mark tests as "cancelled" or "skipped"** without user approval
- ❌ **NEVER commit code with failing tests**
- ❌ **NEVER disable tests** without documenting the reason

**Minimum Test Count for Major Features:**
- **50+ test cases** for major features
- **10+ test scenarios** covering:
  1. Happy path (feature enabled)
  2. Feature disabled scenarios
  3. Invalid input scenarios
  4. Edge cases
  5. Error conditions
  6. Integration points
  7. State changes
  8. Validation rules
  9. Business logic
  10. E2E critical flows

---

## Testing Philosophy

**Why We Test:**
- Catch bugs before production
- Document expected behavior
- Enable confident refactoring
- Serve as living documentation

**What We Test:**
- Business logic (always)
- Edge cases and error conditions (always)
- Integration points (important paths)
- UI critical user flows (key features)
- Configuration behavior (feature flags, settings)
- Validation logic (input validation, business rules)
- State management (status transitions, data flow)
- Error handling (exceptions, failures, retries)

**What We Don't Test:**
- Third-party library internals
- Framework code
- Trivial getters/setters
- Code that just calls other code

---

## Test Structure

### The AAA Pattern (Arrange, Act, Assert)

**Every test should follow this structure:**

```javascript
test('should calculate discounted price for premium users', () => {
  // ARRANGE: Set up test data and dependencies
  const product = { price: 100, name: 'Widget' };
  const premiumUser = { tier: 'premium', discount: 0.2 };
  
  // ACT: Execute the code being tested
  const finalPrice = calculatePrice(product, premiumUser);
  
  // ASSERT: Verify the outcome
  expect(finalPrice).toBe(80);
});
```

Works in any language:

```python
def test_calculate_discounted_price_for_premium_users():
    # Arrange
    product = Product(price=100, name='Widget')
    premium_user = User(tier='premium', discount=0.2)
    
    # Act
    final_price = calculate_price(product, premium_user)
    
    # Assert
    assert final_price == 80
```

---

## Test Naming

### Format: `test_[what]_[scenario]_[expected]`

```javascript
// ✅ Good test names - describe behavior
test('should return empty array when no users exist')
test('should throw error when email is invalid')
test('should calculate tax correctly for CA addresses')
test('should retry failed requests up to 3 times')

// ❌ Bad test names - vague or unclear
test('user test')
test('test1')
test('it works')
test('should work correctly')
```

**Good names answer these questions:**
1. What are you testing?
2. Under what circumstances?
3. What should happen?

---

## Test Coverage

### Levels of Testing

**Unit Tests (Majority of tests)**
- Test individual functions/methods
- Fast, isolated, no external dependencies
- Use mocks for dependencies

**Integration Tests (Some tests)**
- Test multiple components working together
- May use real database/API calls
- Slower but more realistic

**E2E Tests (Few tests)**
- Test complete user workflows
- Slowest, most brittle, most valuable for critical paths

**Pyramid Pattern:**
```
     /\      E2E Tests (Few - Critical flows)
    /  \
   /____\    Integration Tests (Some - Key interactions)
  /      \
 /________\  Unit Tests (Many - All logic)
```

---

## Writing Good Tests

### Test One Thing

```javascript
// ❌ Bad - testing multiple things
test('user registration', () => {
  const user = registerUser(validData);
  expect(user).toBeDefined();
  expect(user.email).toBe(validData.email);
  expect(sendEmail).toHaveBeenCalled();
  expect(database.save).toHaveBeenCalled();
  expect(analytics.track).toHaveBeenCalled();
});

// ✅ Good - separate focused tests
test('should create user with provided email', () => {
  const user = registerUser(validData);
  expect(user.email).toBe(validData.email);
});

test('should send welcome email on registration', () => {
  registerUser(validData);
  expect(sendEmail).toHaveBeenCalledWith(validData.email);
});

test('should save user to database', () => {
  registerUser(validData);
  expect(database.save).toHaveBeenCalled();
});
```

### Make Tests Independent

```python
# ❌ Bad - tests depend on each other
class TestUserFlow:
    user = None
    
    def test_1_create_user(self):
        self.user = create_user("alice@example.com")
        assert self.user is not None
    
    def test_2_update_user(self):
        # Depends on test_1 running first!
        update_user(self.user, name="Alice")
        assert self.user.name == "Alice"

# ✅ Good - each test is independent
class TestUserFlow:
    def test_create_user(self):
        user = create_user("alice@example.com")
        assert user is not None
    
    def test_update_user(self):
        user = create_user("alice@example.com")
        update_user(user, name="Alice")
        assert user.name == "Alice"
```

### Test Edge Cases

```javascript
describe('divide', () => {
  test('should divide positive numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });
  
  test('should handle division resulting in decimal', () => {
    expect(divide(5, 2)).toBe(2.5);
  });
  
  test('should throw error when dividing by zero', () => {
    expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
  });
  
  test('should handle negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
  });
  
  test('should handle zero dividend', () => {
    expect(divide(0, 5)).toBe(0);
  });
});
```

---

## Mocking

### When to Mock

**Mock:**
- External APIs
- Databases
- File system operations
- Time/Date operations
- Random number generation
- External services

**Don't Mock:**
- The code you're testing
- Simple data structures
- Pure functions
- Internal logic

### Mocking Examples

```javascript
// JavaScript with Jest
describe('UserService', () => {
  test('should fetch user from API', async () => {
    // Mock the fetch function
    const mockFetch = jest.fn().mockResolvedValue({
      json: () => Promise.resolve({ id: 1, name: 'Alice' })
    });
    global.fetch = mockFetch;
    
    const user = await userService.getUser(1);
    
    expect(user.name).toBe('Alice');
    expect(mockFetch).toHaveBeenCalledWith('/api/users/1');
  });
});
```

```python
# Python with unittest.mock
from unittest.mock import Mock, patch

def test_should_send_email_notification():
    # Mock the email service
    mock_email_service = Mock()
    notification_service = NotificationService(mock_email_service)
    
    notification_service.notify_user('user@example.com', 'Welcome!')
    
    mock_email_service.send.assert_called_once_with(
        to='user@example.com',
        subject='Welcome!'
    )
```

---

## Test Data

### Use Meaningful Test Data

```javascript
// ❌ Bad - unclear test data
test('should validate user', () => {
  const user = { a: 'x', b: 123, c: true };
  expect(validate(user)).toBe(true);
});

// ✅ Good - clear, realistic test data
test('should validate user with all required fields', () => {
  const validUser = {
    email: 'alice@example.com',
    age: 25,
    acceptedTerms: true
  };
  expect(validate(validUser)).toBe(true);
});
```

### Create Test Helpers

```javascript
// Create helper functions for common test data
function createValidUser(overrides = {}) {
  return {
    email: 'test@example.com',
    name: 'Test User',
    age: 30,
    ...overrides
  };
}

test('should reject user under 18', () => {
  const minorUser = createValidUser({ age: 17 });
  expect(validate(minorUser)).toBe(false);
});

test('should accept user over 18', () => {
  const adultUser = createValidUser({ age: 18 });
  expect(validate(adultUser)).toBe(true);
});
```

---

## Async Testing

```javascript
// ✅ Using async/await (recommended)
test('should fetch user data', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('Alice');
});

// ✅ Using promises
test('should fetch user data', () => {
  return fetchUser(1).then(user => {
    expect(user.name).toBe('Alice');
  });
});

// ❌ Missing return or await - test passes even if assertion fails!
test('should fetch user data', () => {
  fetchUser(1).then(user => {
    expect(user.name).toBe('Alice');
  });
  // Test finishes before promise resolves!
});
```

---

## Test Organization

### Group Related Tests

```javascript
describe('UserService', () => {
  describe('registration', () => {
    test('should create user with valid data');
    test('should reject invalid email');
    test('should reject weak password');
  });
  
  describe('authentication', () => {
    test('should login with correct credentials');
    test('should reject incorrect password');
    test('should lock account after 5 failed attempts');
  });
});
```

### Setup and Teardown

```javascript
describe('DatabaseTests', () => {
  let database;
  
  // Run before each test
  beforeEach(async () => {
    database = await createTestDatabase();
    await database.seed();
  });
  
  // Run after each test
  afterEach(async () => {
    await database.cleanup();
  });
  
  test('should save user to database', async () => {
    await database.users.save({ name: 'Alice' });
    const users = await database.users.findAll();
    expect(users).toHaveLength(1);
  });
});
```

---

## Common Testing Patterns

### Testing Errors

```javascript
// Testing that an error is thrown
test('should throw error for invalid input', () => {
  expect(() => {
    processData(null);
  }).toThrow('Input cannot be null');
});

// Async error testing
test('should reject promise for invalid input', async () => {
  await expect(processDataAsync(null))
    .rejects
    .toThrow('Input cannot be null');
});
```

### Testing State Changes

```javascript
test('should update user count when user is added', () => {
  const store = createStore();
  expect(store.getUserCount()).toBe(0);
  
  store.addUser({ name: 'Alice' });
  expect(store.getUserCount()).toBe(1);
  
  store.addUser({ name: 'Bob' });
  expect(store.getUserCount()).toBe(2);
});
```

### Parameterized Tests

```javascript
// Test multiple cases with similar logic
test.each([
  { input: 'hello', expected: 'HELLO' },
  { input: 'World', expected: 'WORLD' },
  { input: '123', expected: '123' },
  { input: '', expected: '' },
])('should convert "$input" to "$expected"', ({ input, expected }) => {
  expect(toUpperCase(input)).toBe(expected);
});
```

```python
# Python with pytest
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("123", "123"),
    ("", ""),
])
def test_to_uppercase(input, expected):
    assert to_uppercase(input) == expected
```

---

## Test Maintenance

### Keep Tests Updated

- Update tests when requirements change
- Remove obsolete tests
- Refactor tests as code evolves
- Don't let test code quality deteriorate

### Failing Tests

- **Fix failing tests immediately**
- Never commit code with failing tests
- Don't disable tests without good reason
- Investigate flaky tests and fix root cause

---

## Framework-Specific Tips

### JavaScript/TypeScript (Jest/Vitest)

```javascript
// Use descriptive matchers
expect(value).toBe(expected);        // Strict equality
expect(value).toEqual(expected);     // Deep equality
expect(value).toBeTruthy();
expect(value).toHaveLength(3);
expect(array).toContain(item);
expect(string).toMatch(/pattern/);

// Snapshot testing (use sparingly)
expect(component).toMatchSnapshot();
```

### Python (pytest/unittest)

```python
# pytest assertions
assert value == expected
assert value is True
assert len(collection) == 3
assert item in collection

# unittest assertions
self.assertEqual(value, expected)
self.assertTrue(condition)
self.assertIn(item, collection)
self.assertRaises(ValueError, func, args)
```

---

## Testing Checklist

Before considering code "done":
- [ ] Unit tests exist for new logic (MANDATORY)
- [ ] Minimum test count met (10+ scenarios, 50+ cases for major features)
- [ ] Coverage targets met (90%+ unit, 85%+ integration)
- [ ] Edge cases are covered
- [ ] Error conditions are tested
- [ ] Happy path tested
- [ ] Feature flag enabled/disabled scenarios tested
- [ ] Invalid input scenarios tested
- [ ] Integration points tested
- [ ] State changes tested
- [ ] All tests pass (ZERO FAILURES)
- [ ] Tests are readable and maintainable
- [ ] Test names clearly describe what's being tested
- [ ] No skipped or disabled tests without explicit user approval
- [ ] Test coverage meets project standards (90%+ unit, 85%+ integration)

---

## Test Organization Best Practices

### Test File Structure

**Organize by feature and aspect:**
```
tests/
├── unit/
│   ├── {Feature}ValidationTest.*    # Validation tests
│   ├── {Feature}BusinessLogicTest.* # Business logic tests
│   └── {Feature}UtilsTest.*         # Utility function tests
├── integration/
│   ├── {Feature}IntegrationTest.*   # Integration tests
│   └── {Feature}APITest.*           # API tests
└── e2e/
    └── {Feature}E2ETest.*           # End-to-end tests
```

### Test Naming Convention

**Format:** `test{What}{Scenario}{Expected}`

**Examples:**
```javascript
// Unit tests
testUserValidationAcceptsValidEmail()
testUserValidationRejectsInvalidEmail()
testFeatureFlagEnabledAllowsAccess()
testFeatureFlagDisabledDeniesAccess()

// Integration tests
testFullUserRegistrationFlowWithValidData()
testPaymentProcessorBypassForZeroAmount()

// E2E tests
testCompleteCheckoutFlowWithMultipleItems()
testUserLoginAndProfileUpdate()
```

---

## Common Test Scenarios

### 1. Feature Flag Testing

**ALWAYS test both states:**
```javascript
describe('Feature Flag: NewFeature', () => {
  test('should allow feature when flag enabled', () => {
    setFeatureFlag('newFeature', true);
    expect(useNewFeature()).toBe(true);
  });
  
  test('should deny feature when flag disabled', () => {
    setFeatureFlag('newFeature', false);
    expect(useNewFeature()).toBe(false);
  });
});
```

### 2. Validation Testing

**Test all validation rules:**
```javascript
describe('Input Validation', () => {
  test('should accept valid input');
  test('should reject null input');
  test('should reject empty string');
  test('should reject invalid format');
  test('should reject out-of-range values');
  test('should handle special characters');
});
```

### 3. Business Logic Testing

**Cover all business rules:**
```javascript
describe('Business Logic', () => {
  test('should apply discount for premium users');
  test('should not apply discount for regular users');
  test('should calculate tax correctly for each region');
  test('should enforce minimum order value');
  test('should handle edge case: exactly minimum value');
});
```

### 4. Integration Point Testing

**Test external dependencies:**
```javascript
describe('API Integration', () => {
  test('should successfully call external API');
  test('should retry on temporary failure');
  test('should handle API timeout');
  test('should handle API error response');
  test('should handle network failure');
});
```

### 5. State Management Testing

**Test state transitions:**
```javascript
describe('Status Workflow', () => {
  test('should transition from Pending to Processing');
  test('should transition from Processing to Complete');
  test('should not allow transition from Complete to Pending');
  test('should handle concurrent state changes');
});
```

---

## Customize This Template!

**Add your specific needs:**
- Testing framework syntax for your language
- Project-specific test helpers
- CI/CD testing requirements
- Coverage thresholds
- Performance testing standards
- E2E testing patterns
