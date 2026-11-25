---
name: Test-Driven Development (TDD)
description: Master the Test-Driven Development approach with Red-Green-Refactor cycles, writing tests before code, comprehensive coverage patterns, and quality code practices for building robust, maintainable software.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [tdd, red-green-refactor, unit-testing, test-first, refactoring, quality-code, best-practices]
testingTypes: [unit, integration, functional]
frameworks: [jest, pytest, junit, vitest, mocha]
languages: [typescript, javascript, python, java]
domains: [web, api, mobile, backend]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Test-Driven Development (TDD) Skill

You are an expert in Test-Driven Development (TDD), a software development approach where tests are written before the code they validate. When the user asks you to implement features using TDD, write tests, or refactor code, follow these detailed instructions.

## Core Principles

1. **Red-Green-Refactor cycle** -- Write failing test (Red) → Make it pass (Green) → Improve code (Refactor).
2. **Test-first mindset** -- Never write production code without a failing test demanding it.
3. **Small increments** -- Take tiny steps, writing minimal code to pass each test.
4. **Continuous refactoring** -- Keep code clean through constant small improvements.
5. **Fast feedback** -- Tests must run quickly to maintain development flow.

## The TDD Cycle

### Red Phase: Write a Failing Test

Write the smallest test that specifies the next bit of functionality.

```typescript
// Example: Calculator addition feature
describe('Calculator', () => {
  it('should add two positive numbers', () => {
    const calculator = new Calculator();
    expect(calculator.add(2, 3)).toBe(5);
  });
});
```

**Run the test** → It should fail (Red) because `Calculator` doesn't exist yet.

### Green Phase: Make It Pass

Write the minimal code to make the test pass. Don't worry about perfection.

```typescript
class Calculator {
  add(a: number, b: number): number {
    return 5; // Hardcoded to make test pass
  }
}
```

**Run the test** → It should pass (Green).

### Refactor Phase: Improve the Code

Now make the code better while keeping tests green.

```typescript
class Calculator {
  add(a: number, b: number): number {
    return a + b; // Proper implementation
  }
}
```

**Run the test** → Still passes. Safe to refactor.

### Repeat: Add More Tests

```typescript
describe('Calculator', () => {
  it('should add two positive numbers', () => {
    const calculator = new Calculator();
    expect(calculator.add(2, 3)).toBe(5);
  });

  it('should add negative numbers', () => {
    const calculator = new Calculator();
    expect(calculator.add(-2, -3)).toBe(-5);
  });

  it('should add zero', () => {
    const calculator = new Calculator();
    expect(calculator.add(5, 0)).toBe(5);
  });
});
```

## TDD in Different Languages

### JavaScript/TypeScript with Jest/Vitest

```typescript
// tests/user-service.test.ts
import { UserService } from '../src/user-service';
import { User } from '../src/types';

describe('UserService', () => {
  let userService: UserService;

  beforeEach(() => {
    userService = new UserService();
  });

  describe('createUser', () => {
    it('should create a user with valid data', () => {
      const userData = {
        email: 'user@example.com',
        name: 'John Doe',
        age: 30,
      };

      const user = userService.createUser(userData);

      expect(user.id).toBeDefined();
      expect(user.email).toBe('user@example.com');
      expect(user.name).toBe('John Doe');
      expect(user.createdAt).toBeInstanceOf(Date);
    });

    it('should throw error for invalid email', () => {
      const userData = {
        email: 'invalid-email',
        name: 'John Doe',
        age: 30,
      };

      expect(() => userService.createUser(userData)).toThrow('Invalid email format');
    });

    it('should throw error for age below 18', () => {
      const userData = {
        email: 'user@example.com',
        name: 'Young User',
        age: 15,
      };

      expect(() => userService.createUser(userData)).toThrow('User must be at least 18 years old');
    });
  });

  describe('getUserById', () => {
    it('should return user when found', () => {
      const createdUser = userService.createUser({
        email: 'user@example.com',
        name: 'John Doe',
        age: 30,
      });

      const foundUser = userService.getUserById(createdUser.id);

      expect(foundUser).toEqual(createdUser);
    });

    it('should return null when user not found', () => {
      const user = userService.getUserById('non-existent-id');

      expect(user).toBeNull();
    });
  });

  describe('updateUser', () => {
    it('should update user fields', () => {
      const user = userService.createUser({
        email: 'user@example.com',
        name: 'John Doe',
        age: 30,
      });

      const updated = userService.updateUser(user.id, {
        name: 'Jane Doe',
        age: 31,
      });

      expect(updated.name).toBe('Jane Doe');
      expect(updated.age).toBe(31);
      expect(updated.email).toBe('user@example.com'); // Unchanged
    });

    it('should throw error when updating non-existent user', () => {
      expect(() =>
        userService.updateUser('non-existent-id', { name: 'New Name' })
      ).toThrow('User not found');
    });
  });

  describe('deleteUser', () => {
    it('should delete user and return true', () => {
      const user = userService.createUser({
        email: 'user@example.com',
        name: 'John Doe',
        age: 30,
      });

      const deleted = userService.deleteUser(user.id);

      expect(deleted).toBe(true);
      expect(userService.getUserById(user.id)).toBeNull();
    });

    it('should return false when deleting non-existent user', () => {
      const deleted = userService.deleteUser('non-existent-id');

      expect(deleted).toBe(false);
    });
  });
});
```

**Implementation driven by tests:**

```typescript
// src/user-service.ts
import { v4 as uuidv4 } from 'uuid';
import { User, CreateUserData, UpdateUserData } from './types';

export class UserService {
  private users: Map<string, User> = new Map();

  createUser(data: CreateUserData): User {
    // Validation driven by tests
    if (!this.isValidEmail(data.email)) {
      throw new Error('Invalid email format');
    }

    if (data.age < 18) {
      throw new Error('User must be at least 18 years old');
    }

    const user: User = {
      id: uuidv4(),
      email: data.email,
      name: data.name,
      age: data.age,
      createdAt: new Date(),
    };

    this.users.set(user.id, user);
    return user;
  }

  getUserById(id: string): User | null {
    return this.users.get(id) || null;
  }

  updateUser(id: string, data: UpdateUserData): User {
    const user = this.getUserById(id);

    if (!user) {
      throw new Error('User not found');
    }

    const updated = { ...user, ...data };
    this.users.set(id, updated);
    return updated;
  }

  deleteUser(id: string): boolean {
    return this.users.delete(id);
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}
```

### Python with pytest

```python
# tests/test_shopping_cart.py
import pytest
from src.shopping_cart import ShoppingCart, Product

class TestShoppingCart:
    """Shopping cart TDD test suite."""

    @pytest.fixture
    def cart(self):
        """Provide fresh cart for each test."""
        return ShoppingCart()

    @pytest.fixture
    def product(self):
        """Provide sample product."""
        return Product(id="1", name="Widget", price=29.99)

    def test_new_cart_is_empty(self, cart):
        """New shopping cart should be empty."""
        assert cart.is_empty() is True
        assert cart.total_items() == 0
        assert cart.total_price() == 0.0

    def test_add_product_to_cart(self, cart, product):
        """Should add product to cart."""
        cart.add(product)

        assert cart.is_empty() is False
        assert cart.total_items() == 1
        assert cart.contains(product.id) is True

    def test_add_multiple_quantities(self, cart, product):
        """Should handle multiple quantities of same product."""
        cart.add(product, quantity=3)

        assert cart.total_items() == 3
        assert cart.get_quantity(product.id) == 3

    def test_remove_product_from_cart(self, cart, product):
        """Should remove product from cart."""
        cart.add(product)
        cart.remove(product.id)

        assert cart.is_empty() is True
        assert cart.contains(product.id) is False

    def test_update_product_quantity(self, cart, product):
        """Should update product quantity."""
        cart.add(product, quantity=2)
        cart.update_quantity(product.id, 5)

        assert cart.get_quantity(product.id) == 5
        assert cart.total_items() == 5

    def test_calculate_total_price(self, cart):
        """Should calculate correct total price."""
        product1 = Product(id="1", name="Widget A", price=10.00)
        product2 = Product(id="2", name="Widget B", price=15.50)

        cart.add(product1, quantity=2)
        cart.add(product2, quantity=1)

        assert cart.total_price() == 35.50

    def test_apply_discount_code(self, cart, product):
        """Should apply valid discount code."""
        cart.add(product, quantity=2)  # Total: 59.98

        cart.apply_discount("SAVE10")

        assert cart.get_discount() == 5.998  # 10% discount
        assert cart.total_price() == 53.982

    def test_reject_invalid_discount_code(self, cart, product):
        """Should reject invalid discount code."""
        cart.add(product)

        with pytest.raises(ValueError, match="Invalid discount code"):
            cart.apply_discount("INVALID")

    def test_clear_cart(self, cart, product):
        """Should clear all items from cart."""
        cart.add(product, quantity=3)
        cart.clear()

        assert cart.is_empty() is True
        assert cart.total_items() == 0
        assert cart.total_price() == 0.0

    @pytest.mark.parametrize("quantity,expected", [
        (0, "Quantity must be positive"),
        (-1, "Quantity must be positive"),
        (1001, "Quantity exceeds maximum allowed"),
    ])
    def test_invalid_quantities(self, cart, product, quantity, expected):
        """Should validate product quantities."""
        with pytest.raises(ValueError, match=expected):
            cart.add(product, quantity=quantity)
```

**Implementation:**

```python
# src/shopping_cart.py
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Product:
    """Product model."""
    id: str
    name: str
    price: float

class ShoppingCart:
    """Shopping cart with TDD-driven implementation."""

    MAX_QUANTITY = 1000
    DISCOUNT_CODES = {
        "SAVE10": 0.10,
        "SAVE20": 0.20,
    }

    def __init__(self):
        self._items: Dict[str, tuple[Product, int]] = {}
        self._discount_rate: float = 0.0

    def is_empty(self) -> bool:
        """Check if cart is empty."""
        return len(self._items) == 0

    def total_items(self) -> int:
        """Get total number of items."""
        return sum(quantity for _, quantity in self._items.values())

    def add(self, product: Product, quantity: int = 1) -> None:
        """Add product to cart."""
        self._validate_quantity(quantity)

        if product.id in self._items:
            existing_product, existing_qty = self._items[product.id]
            self._items[product.id] = (product, existing_qty + quantity)
        else:
            self._items[product.id] = (product, quantity)

    def remove(self, product_id: str) -> None:
        """Remove product from cart."""
        if product_id in self._items:
            del self._items[product_id]

    def contains(self, product_id: str) -> bool:
        """Check if product is in cart."""
        return product_id in self._items

    def get_quantity(self, product_id: str) -> int:
        """Get quantity of specific product."""
        if product_id in self._items:
            _, quantity = self._items[product_id]
            return quantity
        return 0

    def update_quantity(self, product_id: str, quantity: int) -> None:
        """Update quantity of product."""
        self._validate_quantity(quantity)

        if product_id in self._items:
            product, _ = self._items[product_id]
            self._items[product_id] = (product, quantity)

    def total_price(self) -> float:
        """Calculate total price with discount."""
        subtotal = sum(
            product.price * quantity
            for product, quantity in self._items.values()
        )
        return subtotal - self.get_discount()

    def get_discount(self) -> float:
        """Calculate discount amount."""
        subtotal = sum(
            product.price * quantity
            for product, quantity in self._items.values()
        )
        return subtotal * self._discount_rate

    def apply_discount(self, code: str) -> None:
        """Apply discount code."""
        if code not in self.DISCOUNT_CODES:
            raise ValueError("Invalid discount code")

        self._discount_rate = self.DISCOUNT_CODES[code]

    def clear(self) -> None:
        """Clear all items from cart."""
        self._items.clear()
        self._discount_rate = 0.0

    def _validate_quantity(self, quantity: int) -> None:
        """Validate product quantity."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if quantity > self.MAX_QUANTITY:
            raise ValueError("Quantity exceeds maximum allowed")
```

### Java with JUnit

```java
// tests/OrderServiceTest.java
package com.example.tests;

import com.example.Order;
import com.example.OrderService;
import com.example.OrderStatus;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

class OrderServiceTest {

    private OrderService orderService;

    @BeforeEach
    void setUp() {
        orderService = new OrderService();
    }

    @Test
    @DisplayName("Should create order with valid data")
    void shouldCreateOrderWithValidData() {
        String customerId = "customer-123";
        double amount = 99.99;

        Order order = orderService.createOrder(customerId, amount);

        assertNotNull(order.getId());
        assertEquals(customerId, order.getCustomerId());
        assertEquals(amount, order.getAmount());
        assertEquals(OrderStatus.PENDING, order.getStatus());
        assertNotNull(order.getCreatedAt());
    }

    @ParameterizedTest
    @ValueSource(doubles = {0.0, -10.0, -100.0})
    @DisplayName("Should reject orders with non-positive amounts")
    void shouldRejectNonPositiveAmounts(double amount) {
        String customerId = "customer-123";

        assertThrows(
            IllegalArgumentException.class,
            () -> orderService.createOrder(customerId, amount),
            "Amount must be positive"
        );
    }

    @Test
    @DisplayName("Should reject orders with null customer ID")
    void shouldRejectNullCustomerId() {
        assertThrows(
            IllegalArgumentException.class,
            () -> orderService.createOrder(null, 99.99),
            "Customer ID is required"
        );
    }

    @Test
    @DisplayName("Should process pending order")
    void shouldProcessPendingOrder() {
        Order order = orderService.createOrder("customer-123", 99.99);

        orderService.processOrder(order.getId());

        Order processed = orderService.getOrderById(order.getId());
        assertEquals(OrderStatus.PROCESSING, processed.getStatus());
    }

    @Test
    @DisplayName("Should complete processed order")
    void shouldCompleteProcessedOrder() {
        Order order = orderService.createOrder("customer-123", 99.99);
        orderService.processOrder(order.getId());

        orderService.completeOrder(order.getId());

        Order completed = orderService.getOrderById(order.getId());
        assertEquals(OrderStatus.COMPLETED, completed.getStatus());
        assertNotNull(completed.getCompletedAt());
    }

    @Test
    @DisplayName("Should not complete pending order")
    void shouldNotCompletePendingOrder() {
        Order order = orderService.createOrder("customer-123", 99.99);

        assertThrows(
            IllegalStateException.class,
            () -> orderService.completeOrder(order.getId()),
            "Order must be in PROCESSING status"
        );
    }

    @Test
    @DisplayName("Should cancel pending order")
    void shouldCancelPendingOrder() {
        Order order = orderService.createOrder("customer-123", 99.99);

        orderService.cancelOrder(order.getId());

        Order cancelled = orderService.getOrderById(order.getId());
        assertEquals(OrderStatus.CANCELLED, cancelled.getStatus());
    }

    @Test
    @DisplayName("Should not cancel completed order")
    void shouldNotCancelCompletedOrder() {
        Order order = orderService.createOrder("customer-123", 99.99);
        orderService.processOrder(order.getId());
        orderService.completeOrder(order.getId());

        assertThrows(
            IllegalStateException.class,
            () -> orderService.cancelOrder(order.getId()),
            "Cannot cancel completed order"
        );
    }
}
```

## TDD Best Practices

### 1. Write the Smallest Test First

```typescript
// Start with the simplest case
it('should return empty array for no items', () => {
  const result = filterActiveItems([]);
  expect(result).toEqual([]);
});

// Then add complexity
it('should filter active items', () => {
  const items = [
    { id: 1, active: true },
    { id: 2, active: false },
    { id: 3, active: true },
  ];

  const result = filterActiveItems(items);

  expect(result).toEqual([
    { id: 1, active: true },
    { id: 3, active: true },
  ]);
});
```

### 2. Test One Thing at a Time

```typescript
// BAD: Testing multiple concerns
it('should create user and send welcome email', () => {
  const user = userService.createUser(userData);
  expect(user.id).toBeDefined();
  expect(emailService.sentEmails).toHaveLength(1);
});

// GOOD: Separate tests
it('should create user with generated ID', () => {
  const user = userService.createUser(userData);
  expect(user.id).toBeDefined();
});

it('should send welcome email when user created', () => {
  userService.createUser(userData);
  expect(emailService.sentEmails).toHaveLength(1);
  expect(emailService.sentEmails[0].to).toBe(userData.email);
});
```

### 3. Use Descriptive Test Names

```typescript
// BAD
it('test1', () => { ... });
it('should work', () => { ... });

// GOOD
it('should return empty array when input is empty', () => { ... });
it('should throw error when email is invalid', () => { ... });
it('should calculate total price including tax', () => { ... });
```

### 4. Follow AAA Pattern (Arrange-Act-Assert)

```typescript
it('should add item to cart', () => {
  // Arrange
  const cart = new ShoppingCart();
  const product = { id: '1', name: 'Widget', price: 29.99 };

  // Act
  cart.add(product);

  // Assert
  expect(cart.items).toHaveLength(1);
  expect(cart.items[0]).toEqual(product);
});
```

### 5. Keep Tests Fast

```typescript
// BAD: Real database calls in unit tests
it('should save user to database', async () => {
  const user = await userRepository.save(userData);  // Slow!
  expect(user.id).toBeDefined();
});

// GOOD: Mock external dependencies
it('should save user to database', async () => {
  const mockRepository = {
    save: jest.fn().mockResolvedValue({ id: '123', ...userData })
  };

  const user = await mockRepository.save(userData);  // Fast!
  expect(user.id).toBe('123');
});
```

### 6. Refactor Mercilessly

```typescript
// After tests pass, refactor for clarity

// Before refactoring
function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
}

// After refactoring (tests still pass)
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
```

## Common TDD Patterns

### Test Doubles (Mocks, Stubs, Spies)

```typescript
// Stub: Provides canned responses
const stubRepository = {
  findById: () => ({ id: '123', name: 'Test User' })
};

// Mock: Verifies interactions
const mockEmailService = {
  send: jest.fn()
};
emailService.send('test@example.com', 'Subject', 'Body');
expect(mockEmailService.send).toHaveBeenCalledWith('test@example.com', 'Subject', 'Body');

// Spy: Wraps real object
const spy = jest.spyOn(service, 'method');
service.method();
expect(spy).toHaveBeenCalled();
spy.mockRestore();
```

### Parameterized Tests

```typescript
describe.each([
  { input: 'hello', expected: 'HELLO' },
  { input: 'world', expected: 'WORLD' },
  { input: 'TDD', expected: 'TDD' },
])('toUpperCase', ({ input, expected }) => {
  it(`should convert "${input}" to "${expected}"`, () => {
    expect(toUpperCase(input)).toBe(expected);
  });
});
```

### Test Fixtures

```typescript
class UserServiceTestFixture {
  userService: UserService;
  validUserData: CreateUserData;

  beforeEach() {
    this.userService = new UserService();
    this.validUserData = {
      email: 'user@example.com',
      name: 'John Doe',
      age: 30,
    };
  }

  createValidUser(): User {
    return this.userService.createUser(this.validUserData);
  }
}

describe('UserService', () => {
  const fixture = new UserServiceTestFixture();

  beforeEach(() => fixture.beforeEach());

  it('should create user', () => {
    const user = fixture.createValidUser();
    expect(user.email).toBe('user@example.com');
  });
});
```

## Anti-Patterns to Avoid

1. **Writing tests after code** -- Defeats the purpose of TDD.
2. **Testing implementation details** -- Test behavior, not internals.
3. **Slow tests** -- Tests should run in milliseconds.
4. **Brittle tests** -- Tests that break with unrelated changes.
5. **Testing framework code** -- Don't test libraries; test your code.
6. **Not refactoring** -- Green phase is not the end; refactor!
7. **Large test suites per test** -- One assertion per test is ideal.
8. **Skipping Red phase** -- Always see the test fail first.
9. **Mocking everything** -- Use real objects when practical.
10. **Not cleaning up** -- Reset state between tests.

## TDD for Different Scenarios

### API Endpoint (Express.js)

```typescript
// tests/api/users.test.ts
import request from 'supertest';
import { app } from '../src/app';

describe('POST /api/users', () => {
  it('should create user and return 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'user@example.com',
        name: 'John Doe',
        age: 30,
      })
      .expect(201);

    expect(response.body.id).toBeDefined();
    expect(response.body.email).toBe('user@example.com');
  });

  it('should return 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'invalid-email',
        name: 'John Doe',
        age: 30,
      })
      .expect(400);

    expect(response.body.error).toContain('Invalid email');
  });
});
```

### React Component (Jest + Testing Library)

```typescript
// tests/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../src/components/Button';

describe('Button', () => {
  it('should render with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

## Metrics and Coverage

### Aim for High Coverage

```bash
# Run tests with coverage
npm test -- --coverage

# Target 80%+ coverage
# Uncovered lines indicate missing tests
```

### Focus on Critical Paths

```typescript
// Prioritize testing:
// 1. Business logic
// 2. Error handling
// 3. Edge cases
// 4. Integration points
```

## Integration with AI Agents

When AI agents practice TDD, they should:

1. **Always write tests first** before any implementation code
2. **Run tests frequently** after each small change
3. **Verify tests fail** before writing implementation (Red phase)
4. **Write minimal code** to make tests pass (Green phase)
5. **Refactor continuously** while keeping tests green
6. **Document test intent** with clear descriptions
7. **Maintain fast test execution** for rapid feedback
8. **Clean up test code** as diligently as production code

TDD empowers developers and AI agents to build robust, well-tested software with confidence, ensuring every line of code is justified by a test.
