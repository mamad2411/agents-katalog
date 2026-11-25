---
name: testing-patterns
description: Write comprehensive tests following testing best practices and patterns. Use when writing tests, setting up test infrastructure, or when the user asks about testing, unit tests, integration tests, mocking, or test coverage.
---

# Testing Patterns & Best Practices

Write comprehensive, maintainable tests that provide confidence in code quality and prevent regressions.

## Testing Pyramid

```
        /\
       /  \      E2E Tests (Few)
      /____\
     /      \    Integration Tests (Some)
    /________\
   /          \  Unit Tests (Many)
  /____________\
```

**Unit Tests** - Test individual functions/components in isolation
**Integration Tests** - Test interactions between components
**E2E Tests** - Test complete user workflows

## Unit Testing

### Structure: AAA Pattern

```typescript
describe("OrderService", () => {
  describe("createOrder", () => {
    it("should create an order successfully", () => {
      // Arrange - Set up test data and mocks
      const orderData = { storeId: 1, items: [] };
      const mockRepository = {
        create: jest.fn().mockResolvedValue({ id: 1, ...orderData }),
      };
      const service = new OrderService(mockRepository);

      // Act - Execute the function
      const result = await service.createOrder(orderData);

      // Assert - Verify the outcome
      expect(result).toHaveProperty("id");
      expect(mockRepository.create).toHaveBeenCalledWith(orderData);
    });
  });
});
```

### Test Organization

```typescript
// Group related tests
describe("UserService", () => {
  describe("createUser", () => {
    it("should create user with valid data", () => {});
    it("should throw error for duplicate email", () => {});
    it("should hash password before saving", () => {});
  });

  describe("updateUser", () => {
    it("should update user fields", () => {});
    it("should not update password if not provided", () => {});
  });
});
```

### Naming Conventions

```typescript
// Use descriptive test names
it("should return 404 when user does not exist", () => {});
it("should throw ValidationError when email is invalid", () => {});
it("should send email notification after order creation", () => {});

// Avoid vague names
it("should work", () => {}); // ❌
it("test 1", () => {}); // ❌
```

## Mocking & Stubbing

### Mock External Dependencies

```typescript
// Mock database
jest.mock("../models/User", () => ({
  findById: jest.fn(),
  create: jest.fn(),
}));

// Mock external services
jest.mock("../services/EmailService", () => ({
  sendEmail: jest.fn().mockResolvedValue(true),
}));

// Mock HTTP requests
jest.mock("axios", () => ({
  get: jest.fn(),
  post: jest.fn(),
}));
```

### Mock Functions

```typescript
// Jest mocks
const mockFn = jest.fn();
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ id: 1 });
mockFn.mockRejectedValue(new Error("Failed"));

// Verify calls
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledWith(expectedArgs);
expect(mockFn).toHaveBeenCalledTimes(2);
```

### Partial Mocks

```typescript
// Mock only specific methods
const userService = {
  getUser: jest.fn(),
  createUser: jest.fn(),
  // Other methods remain real
};

// Or use jest.spyOn
const spy = jest.spyOn(userService, "getUser");
spy.mockResolvedValue({ id: 1 });
```

## Integration Testing

### Test API Endpoints

```typescript
describe("POST /users", () => {
  it("should create a user", async () => {
    const response = await request(app)
      .post("/users")
      .send({
        email: "test@example.com",
        password: "password123",
      })
      .expect(201);

    expect(response.body.data).toHaveProperty("id");
    expect(response.body.data.email).toBe("test@example.com");
  });

  it("should return 400 for invalid data", async () => {
    const response = await request(app)
      .post("/users")
      .send({ email: "invalid" })
      .expect(400);

    expect(response.body.error).toBeDefined();
  });
});
```

### Test Database Interactions

```typescript
describe("UserRepository", () => {
  beforeEach(async () => {
    // Set up test database
    await db.sequelize.sync({ force: true });
  });

  afterEach(async () => {
    // Clean up
    await db.sequelize.truncate();
  });

  it("should save and retrieve user", async () => {
    const user = await User.create({
      email: "test@example.com",
      password: "hashed",
    });

    const found = await User.findById(user.id);
    expect(found.email).toBe("test@example.com");
  });
});
```

## Test Data Management

### Factories

```typescript
// factories/userFactory.ts
export const createUser = (overrides = {}) => ({
  email: "user@example.com",
  password: "password123",
  name: "Test User",
  ...overrides,
});

// Usage
const user = createUser({ email: "custom@example.com" });
```

### Fixtures

```typescript
// fixtures/users.ts
export const users = {
  admin: {
    email: "admin@example.com",
    role: "admin",
  },
  customer: {
    email: "customer@example.com",
    role: "customer",
  },
};
```

## Testing Best Practices

### 1. Test One Thing at a Time

```typescript
// ✅ Good - One assertion per concept
it('should calculate total price', () => {
  const total = calculateTotal([{ price: 10 }, { price: 20 }]);
  expect(total).toBe(30);
});

// ❌ Bad - Multiple unrelated assertions
it('should do everything', () => {
  expect(calculateTotal([...])).toBe(30);
  expect(validateEmail('test@example.com')).toBe(true);
  expect(formatDate(new Date())).toBe('2024-01-01');
});
```

### 2. Use Descriptive Test Names

```typescript
// ✅ Good
it("should throw ValidationError when email is missing", () => {});
it("should return user orders sorted by createdAt descending", () => {});

// ❌ Bad
it("test 1", () => {});
it("works", () => {});
```

### 3. Test Edge Cases

```typescript
describe("divide", () => {
  it("should divide two numbers", () => {
    expect(divide(10, 2)).toBe(5);
  });

  it("should throw error when dividing by zero", () => {
    expect(() => divide(10, 0)).toThrow("Cannot divide by zero");
  });

  it("should handle negative numbers", () => {
    expect(divide(-10, 2)).toBe(-5);
  });
});
```

### 4. Keep Tests Independent

```typescript
// ✅ Good - Each test is independent
describe("UserService", () => {
  beforeEach(() => {
    // Set up fresh state for each test
  });

  it("test 1", () => {});
  it("test 2", () => {}); // Doesn't depend on test 1
});

// ❌ Bad - Tests depend on each other
let sharedState;
it("test 1", () => {
  sharedState = "value";
});
it("test 2", () => {
  expect(sharedState).toBe("value"); // Depends on test 1
});
```

### 5. Test Behavior, Not Implementation

```typescript
// ✅ Good - Test what the function does
it("should return user by id", async () => {
  const user = await service.getUser(123);
  expect(user).toHaveProperty("id", 123);
});

// ❌ Bad - Test implementation details
it("should call repository.findById", async () => {
  await service.getUser(123);
  expect(repository.findById).toHaveBeenCalled(); // Too specific
});
```

### 6. Use Test Doubles Appropriately

```typescript
// Stub - Replace with simpler implementation
const stub = jest.fn().mockReturnValue(42);

// Mock - Verify interactions
const mock = jest.fn();
expect(mock).toHaveBeenCalled();

// Spy - Observe real implementation
const spy = jest.spyOn(service, "method");
```

## Test Coverage

### Aim for High Coverage

- **Statements**: 80%+
- **Branches**: 75%+
- **Functions**: 80%+
- **Lines**: 80%+

### Coverage Tools

```typescript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageThreshold: {
    global: {
      branches: 75,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

## Testing Async Code

### Promises

```typescript
it("should handle async operations", async () => {
  const result = await asyncFunction();
  expect(result).toBeDefined();
});

// Or with .then()
it("should handle promises", () => {
  return asyncFunction().then((result) => {
    expect(result).toBeDefined();
  });
});
```

### Error Handling

```typescript
it("should throw error", async () => {
  await expect(asyncFunction()).rejects.toThrow("Error message");
});

// Or
it("should throw error", async () => {
  try {
    await asyncFunction();
    fail("Should have thrown");
  } catch (error) {
    expect(error.message).toBe("Error message");
  }
});
```

## When Writing Tests

1. **Write tests first (TDD)** - Red, Green, Refactor
2. **Test edge cases** - Null, empty, boundary values
3. **Test error cases** - Invalid inputs, failures
4. **Keep tests fast** - Mock slow operations
5. **Keep tests isolated** - No shared state
6. **Use descriptive names** - Clear what is being tested
7. **Arrange-Act-Assert** - Clear test structure
8. **Mock external dependencies** - Isolate unit under test
9. **Test behavior, not implementation** - Focus on outcomes
10. **Maintain test code** - Refactor tests like production code
