---
name: testing-strategies
description: Design and implement comprehensive testing strategies covering unit, integration, and E2E tests. Maximize coverage and confidence.
triggers:
- /testing
- /test strategy
---

# Testing Strategies

This skill guides you through designing and implementing comprehensive testing strategies including unit tests, integration tests, and end-to-end tests.

## When to use this skill

Use this skill when you need to:
- Design a testing strategy for a project
- Write effective unit tests
- Implement integration tests
- Set up end-to-end testing
- Improve test coverage and quality

## Prerequisites

- Testing framework for your language (pytest, Jest, NUnit, Go testing)
- Understanding of the application architecture
- CI/CD pipeline for running tests
- Code coverage tools

## Guidelines

### Testing Pyramid

```
      /\
     /  \
    / E2E \          (Few tests, high confidence, slow)
   /--------\
  /Integration\      (Medium tests, medium confidence)
 /--------------\
/    Unit Tests   \   (Many tests, fast, focused)
---------------------
```

**Target Distribution**
- Unit tests: 70% of total tests
- Integration tests: 20% of total tests
- E2E tests: 10% of total tests

### Unit Testing

**Principles**
- Test one thing per test
- Tests should be independent
- Use descriptive test names
- Follow Arrange-Act-Assert pattern

**Example (Python with pytest)**
```python
import pytest

def test_calculate_discount_applies_percentage():
    # Arrange
    price = 100.0
    discount_percent = 10
    
    # Act
    result = calculate_discount(price, discount_percent)
    
    # Assert
    assert result == 90.0

def test_calculate_discount_rejects_negative_price():
    with pytest.raises(ValueError, match="Price must be positive"):
        calculate_discount(-10, 10)
```

**Mocking**
- Mock external dependencies (databases, APIs)
- Use dependency injection for testability
- Verify interactions, not just outputs
- Don't mock what you don't own

```python
from unittest.mock import Mock, patch

def test_process_order_sends_notification():
    mock_notifier = Mock()
    service = OrderService(notification_service=mock_notifier)
    
    service.process_order(order)
    
    mock_notifier.send.assert_called_once_with(
        to=order.customer_email,
        subject="Order confirmed"
    )
```

### Integration Testing

**Scope**
- Test component interactions
- Use real (test) database
- Test API endpoints
- Verify data flow through layers

**Database Testing**
```python
@pytest.fixture
db_session():
    # Set up test database
    engine = create_engine("postgresql://test:test@localhost/testdb")
    yield Session(engine)
    # Clean up
    engine.execute("TRUNCATE orders, customers")

def test_order_repository_creates_order(db_session):
    repo = OrderRepository(db_session)
    order = Order(customer_id=1, total=100)
    
    saved_order = repo.save(order)
    
    assert saved_order.id is not None
    assert db_session.query(Order).count() == 1
```

**API Testing**
```python
def test_create_order_endpoint(client):
    response = client.post("/api/orders", json={
        "customer_id": 1,
        "items": [{"product_id": 1, "quantity": 2}]
    })
    
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["status"] == "pending"
```

### End-to-End Testing

**Tools**
- Web: Cypress, Playwright, Selenium
- Mobile: Appium, Detox
- API: Postman/Newman, REST Assured

**Example (Playwright)**
```typescript
import { test, expect } from '@playwright/test';

test('user can complete purchase', async ({ page }) => {
  // Navigate and login
  await page.goto('/login');
  await page.fill('[data-testid=email]', 'user@test.com');
  await page.fill('[data-testid=password]', 'password');
  await page.click('[data-testid=login-button]');
  
  // Add item to cart
  await page.goto('/products');
  await page.click('[data-testid=add-to-cart]');
  
  // Checkout
  await page.goto('/checkout');
  await page.fill('[data-testid=card-number]', '4111111111111111');
  await page.click('[data-testid=place-order]');
  
  // Verify
  await expect(page.locator('[data-testid=success-message]'))
    .toBeVisible();
});
```

### Test Organization

**Folder Structure**
```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_repositories.py
│   ├── test_api.py
│   └── test_external_services.py
├── e2e/
│   ├── test_user_flows.spec.ts
│   └── test_admin_flows.spec.ts
└── fixtures/
    └── test_data.py
```

### Best Practices

**Test Data**
- Use factories (factory_boy, faker)
- Avoid shared test state
- Clean up after each test
- Use in-memory databases where possible

**Flaky Tests**
- Avoid timing-dependent assertions
- Don't rely on external services
- Use test-specific data to avoid conflicts
- Retry with exponential backoff for async operations

**Coverage**
- Aim for 80%+ code coverage
- Focus on critical paths
- Don't chase 100% at expense of maintainability
- Use coverage tools to identify gaps

## Examples

See the `examples/` directory for:
- `unit-test-examples/` - Unit test patterns by language
- `integration-test-setup/` - Database and API testing
- `e2e-playwright/` - End-to-end test suite
- `test-fixtures/` - Reusable test data factories

## References

- [Testing Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [pytest documentation](https://docs.pytest.org/)
- [Jest documentation](https://jestjs.io/)
- [Playwright documentation](https://playwright.dev/)
- [Google testing blog](https://testing.googleblog.com/)
