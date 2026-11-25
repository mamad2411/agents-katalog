name: generate-unit-tests
description: Creates focused Python unit tests with clear assertions and minimal mocking. Use this when you need to generate unit tests for Python functions, methods, or classes using pytest or unittest.

---

# Generate Unit Tests

## Purpose

Create focused Python unit tests with clear assertions and minimal mocking. This skill generates unit tests that verify behavior without coupling to implementation details, using pytest as the primary framework.

## Use when

- Writing unit tests for pure functions or methods
- Testing business logic in isolation
- Creating tests for helper functions and utilities
- Generating tests for refactored code
- Building a fast test suite for CI

## Do not use when

- You need integration tests (use `generate-integration-tests`)
- You're testing external behavior (use e2e tests)
- You need to test database, network, or filesystem interactions

## Inputs

- Python code to test (functions, methods, classes)
- Expected behavior or requirements
- Preferred testing framework (pytest default, unittest optional)
- Any existing test conventions in the project

## Outputs

- Complete test file with pytest-style tests
- Parametrized test cases where appropriate
- Clear test names that describe behavior
- Minimal, focused assertions

## Method

1. **Identify testable units**
   - Extract pure functions and methods
   - Identify public APIs
   - Note dependencies that need mocking

2. **Choose pytest patterns**
   - Use `@pytest.mark.parametrize` for multiple cases
   - Use fixtures for setup/teardown
   - Use markers for test categorization
   - Prefer `assert` over `assertTrue/assertFalse`

3. **Write clear test names**
   - Format: `test_<scenario>_<expected_result>`
   - Example: `test_calculate_discount_high_value_returns_ten_percent`
   - Avoid: `test_function_1`, `test_case_a`

4. **Apply minimal mocking**
   - Mock only external dependencies (DB, API, filesystem)
   - Don't mock internal methods or private helpers
   - Use `unittest.mock.patch` or `pytest-mock`
   - Prefer dependency injection over patching

5. **Write focused assertions**
   - Assert on behavior, not implementation
   - Use descriptive error messages
   - Avoid over-specifying (exact lists, specific order)
   - Test the "what", not the "how"

## Pytest Best Practices

- Use `pytest.raises` for exception testing
- Use `tmp_path` for filesystem tests
- Use `monkeypatch` for environment changes
- Use `caplog` for logging tests
- Use `@pytest.mark.asyncio` for async tests

## Guardrails

- Don't mock things you own (internal methods, private helpers)
- Don't test implementation details (exact call order, internal state)
- Don't write tests that are hard to read or understand
- Avoid testing things the type checker already validates

## Example prompts

```
Generate unit tests for this function using pytest:

```python
def calculate_discount(price: float, user: User) -> float:
    if price > 100 and user.is_premium:
        return price * 0.9
    elif price > 50:
        return price * 0.95
    return price
```

---

Write pytest unit tests for this class:

```python
class ShoppingCart:
    def __init__(self):
        self._items: list[Item] = []
    
    def add_item(self, item: Item) -> None:
        self._items.append(item)
    
    def total(self) -> float:
        return sum(item.price for item in self._items)
    
    def apply_coupon(self, coupon: Coupon) -> None:
        # ...
```

---

Generate unit tests with parametrization for this function:

```python
def parse_date(date_str: str, format: str) -> date:
    return datetime.strptime(date_str, format).date()
```
