name: design-high-value-tests
description: Proposes the minimum high-value Python test set with the strongest regression protection. Use this when you need to design an effective test suite that maximizes bug detection while minimizing test maintenance overhead.

---

# Design High-Value Tests

## Purpose

Propose the minimum high-value Python test set with the strongest regression protection. This skill helps design test suites that catch the most bugs with the fewest tests, prioritizing maintainability and business-critical behavior.

## Use when

- Designing a test strategy for a new Python module
- Creating a regression test suite with limited resources
- Reviewing existing test coverage and prioritizing gaps
- Planning testing efforts for a feature or refactor
- Balancing test coverage with maintenance costs

## Do not use when

- You need to write specific test cases (use `generate-unit-tests` or `generate-integration-tests`)
- You're debugging a specific failure
- You need to find edge cases (use `find-edge-cases` instead)

## Inputs

- Python source code or module structure
- Critical scenarios (from `identify-critical-scenarios`)
- Business context and user workflows
- Existing test coverage (if available)

## Outputs

- Prioritized list of test cases with rationale
- Test level recommendation for each case (unit, integration, e2e)
- Expected bug categories each test catches
- Maintenance cost estimate per test

## Method

1. **Start with critical behaviors**
   - Focus on business-critical paths first
   - Identify the "happy path" for each major feature
   - Note key error conditions that must be handled

2. **Apply the 80/20 rule**
   - Identify the 20% of tests that catch 80% of bugs
   - Prioritize tests that catch regressions, not just verify implementation
   - Avoid tests that only check implementation details

3. **Choose appropriate test levels**
   - Unit tests for pure logic and business rules
   - Integration tests for external dependencies
   - E2e tests for critical user workflows
   - Contract tests for API interfaces

4. **Maximize regression value**
   - Include tests for previously buggy areas
   - Add tests that catch common mistake patterns
   - Cover integration points between modules

5. **Minimize maintenance**
   - Avoid testing implementation details
   - Use descriptive test names that explain intent
   - Prefer parametrized tests over duplicates
   - Avoid fragile assertions (exact strings, specific order)

## Test Value Framework

| Test Type | Bug Detection | Maintenance | When to Include |
|-----------|---------------|-------------|-----------------|
| Critical path happy path | High | Low | Always |
| Critical error handling | High | Low | Always |
| Edge cases with real impact | Medium | Low | Often |
| Implementation details | Low | High | Rarely |
| Private method behavior | Low | High | Never |
| Exact output format | Low | Medium | Only if contract |

## Guardrails

- Don't aim for 100% line coverage; aim for 100% critical path coverage
- Avoid testing things that are hard to break (simple getters, trivial transformations)
- Don't write tests that only verify the compiler/type checker
- Skip tests that would need to be updated with every refactoring

## Example prompts

```
Design a high-value test suite for this module:

```python
class OrderProcessor:
    def __init__(self, payment_gateway: PaymentGateway, inventory: Inventory):
        self.payment = payment_gateway
        self.inventory = inventory
    
    def process_order(self, order: Order) -> OrderResult:
        # Complex business logic...
        pass
```

---

What are the minimum high-value tests for this API endpoint?

```python
@app.post("/api/users")
async def create_user(user: UserCreate):
    # Validation, DB insert, email sending, caching...
    pass
```

---

Design a regression-focused test suite for this refactoring:

```python
# Before: monolithic function
def process_data(raw_data):
    # 200 lines of mixed validation, transformation, and saving

# After: refactored into smaller functions
def validate_data(raw_data): ...
def transform_data(raw_data): ...
def save_data(transformed): ...
```
