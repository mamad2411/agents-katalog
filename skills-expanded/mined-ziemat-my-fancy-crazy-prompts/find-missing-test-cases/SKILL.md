name: find-missing-test-cases
description: Identifies important Python test gaps in existing test suites. Use this when you need to find what's not being tested and prioritize adding tests for uncovered critical paths.

---

# Find Missing Test Cases

## Purpose

Identify important Python test gaps in existing test suites. This skill analyzes code and existing tests to find what's not being tested and prioritizes adding tests for uncovered critical paths.

## Use when

- Reviewing existing test coverage
- Planning test additions for a module
- Preparing for a refactor or migration
- Responding to a bug that wasn't caught by tests
- Auditing test suite completeness

## Do not use when

- You need to write the actual tests (use `generate-unit-tests` or `generate-integration-tests`)
- You're debugging a specific failure
- You need to identify critical scenarios (use `identify-critical-scenarios` instead)

## Inputs

- Python source code
- Existing test files
- Test coverage report (optional but helpful)
- Bug reports or incident history (optional but helpful)

## Outputs

- List of missing test cases with priority
- Coverage gaps by category (happy path, edge cases, errors)
- Recommendations for test additions
- Risk assessment for uncovered areas

## Method

1. **Analyze existing tests**
   - Map existing tests to code paths
   - Identify covered vs uncovered branches
   - Note test coverage by function/method
   - Check for parametrization gaps

2. **Identify coverage gaps**
   - Happy paths without tests
   - Edge cases not covered
   - Error paths not tested
   - Integration points not verified
   - Async code without tests

3. **Prioritize missing tests**
   - P0: Critical paths with no tests
   - P1: Important edge cases or error paths
   - P2: Nice-to-have scenarios

4. **Consider bug history**
   - What bugs weren't caught by tests?
   - What areas had recent fixes?
   - What areas are change-prone?

5. **Generate recommendations**
   - Specific test cases to add
   - Test level for each case
   - Rationale for priority

## Coverage Gap Categories

| Category | What to Look For | Priority |
|----------|------------------|----------|
| **Happy path** | Main functionality not tested | P0 |
| **Edge cases** | Boundary values, empty inputs | P1 |
| **Error handling** | Exception paths, validation | P1 |
| **Integration** | External deps, module boundaries | P1 |
| **Async** | Async code, concurrency | P1 |
| **Documentation** | Docstring examples not tested | P2 |

## Guardrails

- Don't just list every possible test case; prioritize by impact
- Don't recommend testing implementation details
- Consider the cost of adding each test
- Balance completeness with maintainability

## Example prompts

```
Find missing test cases for this module:

```python
class PaymentProcessor:
    def process(self, amount: float, currency: str) -> PaymentResult:
        # ...
    
    def refund(self, transaction_id: str) -> bool:
        # ...
    
    def check_balance(self, user_id: int) -> float:
        # ...
```

Existing tests: Only tests happy path for `process`

---

What test cases are missing from this test suite?

```python
# test_user.py
def test_create_user_valid(): ...
def test_create_user_duplicate(): ...
# Missing: email validation, password strength, edge cases
```

---

Analyze coverage gaps for this function:

```python
def parse_config(path: Path) -> dict:
    # 50 lines of config parsing
    # Multiple error paths, edge cases
```

Current tests: Only tests valid config file
