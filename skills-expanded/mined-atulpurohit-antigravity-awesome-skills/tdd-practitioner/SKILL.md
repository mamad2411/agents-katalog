---
name: tdd-practitioner
description: "Practice Test-Driven Development with the red-green-refactor cycle. Write tests before code to drive better design, coverage, and confidence."
category: testing
tags: [tdd, test-driven, red-green-refactor, unit-tests]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# TDD Practitioner

## Purpose
Write better, more reliable code by letting tests drive the implementation through the red-green-refactor cycle.

## The TDD Cycle

### Red → Green → Refactor

```
1. RED:    Write a failing test for the next small piece of behavior
2. GREEN:  Write the minimum code to make it pass
3. REFACTOR: Clean up without breaking tests
Repeat...
```

### 1️⃣ Writing a Good Unit Test (AAA Pattern)
```python
def test_order_calculates_total_with_discount():
    # ARRANGE: Set up the system under test
    items = [
        OrderItem(product_id="A", quantity=2, price=Money("25.00")),
        OrderItem(product_id="B", quantity=1, price=Money("50.00")),
    ]
    discount = PercentageDiscount(rate=Decimal("0.10"))  # 10% off
    order = Order(items=items, discount=discount)
    
    # ACT: Perform the action
    total = order.calculate_total()
    
    # ASSERT: Verify the outcome
    assert total == Money("90.00")  # (25*2 + 50) * 0.9 = 90
```

### 2️⃣ Test Quality Checklist
- [ ] Tests one thing (single assertion concept)
- [ ] Test name describes behavior: `test_[method]_[scenario]_[expected_result]`
- [ ] Independent — no test depends on another
- [ ] Fast — no I/O, no external calls
- [ ] Deterministic — same result every run
- [ ] Tests behavior, not implementation details

### 3️⃣ Test Doubles
```python
# Mock (verify interactions)
mock_email = Mock()
service = UserService(email_sender=mock_email)
service.register(email="test@example.com")
mock_email.send.assert_called_once_with(
    to="test@example.com",
    subject="Welcome!"
)

# Stub (provide canned responses)
stub_repo = Mock()
stub_repo.find_by_email.return_value = User(id=1, email="test@example.com")

# Fake (simplified working implementation)
class InMemoryOrderRepository:
    def __init__(self): self._store = {}
    def save(self, order): self._store[order.id] = order
    def find(self, id): return self._store.get(id)
```

### 4️⃣ Outside-In TDD (Starting with Acceptance Tests)
```
1. Write failing acceptance test (high level behavior)
2. Write failing unit tests for components needed
3. Implement until unit tests pass
4. Run acceptance test — keep going until it passes
5. Refactor
```

## Outputs
1. Test suite for specified feature
2. Mock/stub configuration
3. Test helpers and builders
4. Coverage report analysis
5. TDD workflow documentation
