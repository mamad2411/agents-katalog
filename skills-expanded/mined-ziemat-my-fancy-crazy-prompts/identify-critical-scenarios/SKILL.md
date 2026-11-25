name: identify-critical-scenarios
description: Identifies the smallest set of critical behaviors in Python code that must not break. Use this when analyzing Python modules, functions, or services to determine which behaviors are business-critical and require test coverage. This skill focuses on identifying what matters most, not how to test it.

---

# Identify Critical Scenarios

## Purpose

Identify the minimal set of critical behaviors in Python code that must not break. This skill analyzes code to find the smallest set of behaviors that, if broken, would cause the most business or technical impact.

## Use when

- Analyzing a new Python module or function before writing tests
- Deciding which behaviors deserve test coverage first
- Performing risk-based testing decisions
- Creating regression test suites with limited resources
- Understanding what "correct behavior" means for a piece of code

## Do not use when

- You already have a complete test suite and are looking for gaps
- You're debugging a specific failing test
- You're writing implementation code (not analyzing behavior)

## Inputs

- Python source code (functions, classes, modules)
- Context about the code's purpose (optional but helpful)
- Any existing documentation or comments

## Outputs

- Ranked list of critical scenarios with priority (P0, P1, P2)
- Brief explanation of why each scenario is critical
- Business or technical impact if the scenario breaks

## Method

1. **Analyze the code structure**
   - Identify public APIs (functions, methods, classes exposed to callers)
   - Find core business logic vs helper/utility code
   - Note exception handling and error paths

2. **Identify critical behaviors**
   - Look for operations that affect external systems (DB, API, filesystem)
   - Find data transformations that affect downstream code
   - Identify validation logic that prevents invalid states
   - Note performance-critical paths

3. **Rank by impact**
   - P0: Must work correctly; breaking causes data loss, security issues, or system failure
   - P1: Important for correct operation; breaking causes degraded functionality
   - P2: Nice-to-have; breaking causes minor inconvenience

4. **Consider edge cases that matter**
   - Invalid inputs that should be rejected
   - Empty collections vs None
   - Boundary values that change behavior
   - Concurrency concerns if applicable

## Guardrails

- Focus on behavior, not implementation details
- Don't list every possible test case; focus on the critical few
- Consider the code's context and purpose
- Avoid over-prioritizing edge cases that are unlikely to occur in production

## Example prompts

```
Analyze this Python function and identify the critical scenarios that must be tested:

```python
def process_payment(amount: float, card_number: str, cvv: str) -> dict:
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if not re.match(r'^\d{16}$', card_number):
        raise ValueError("Invalid card number")
    if not re.match(r'^\d{3,4}$', cvv):
        raise ValueError("Invalid CVV")
    
    # Process payment...
    return {"status": "success", "transaction_id": generate_id()}
```

---

Identify the critical scenarios for this service class:

```python
class UserService:
    def __init__(self, db: Database, cache: Cache):
        self.db = db
        self.cache = cache
    
    def get_user(self, user_id: int) -> User | None:
        # ...
    
    def create_user(self, data: dict) -> User:
        # ...
    
    def delete_user(self, user_id: int) -> bool:
        # ...
```

---

What are the P0 critical scenarios for this data processing function?

```python
def transform_and_save(data: list[dict], schema: Schema) -> int:
    validated = [schema.validate(row) for row in data]
    saved = db.insert_all(validated)
    cache.invalidate("transform_cache")
    return saved
```
