name: choose-test-level
description: Decides whether each Python scenario belongs in unit, integration, end-to-end, or contract tests. Use this when you need to determine the appropriate test level for specific test cases or code components.

---

# Choose Test Level

## Purpose

Decide whether each Python scenario belongs in unit, integration, end-to-end, or contract tests. This skill helps determine the appropriate test level based on what's being tested, dependencies involved, and testing goals.

## Use when

- Planning test cases and deciding their level
- Reviewing existing tests and verifying their level is appropriate
- Setting up a new testing strategy
- Refactoring tests and needing to re-categorize them
- Balancing test suite speed vs coverage

## Do not use when

- You need to write the actual test code (use `generate-unit-tests` or `generate-integration-tests`)
- You're debugging a specific failing test
- You need to identify what to test (use `identify-critical-scenarios` instead)

## Inputs

- Code or functionality to be tested
- Dependencies and external systems involved
- Testing goals (speed, coverage, regression prevention)
- Existing test structure and conventions

## Outputs

- Recommended test level (unit, integration, e2e, contract)
- Rationale for the recommendation
- Alternative options with trade-offs
- Specific considerations for Python implementation

## Method

1. **Identify dependencies**
   - Pure Python functions with no external deps → unit test
   - Database, API, filesystem, network calls → integration test
   - User-facing workflows → e2e test
   - Interface contracts between services → contract test

2. **Consider isolation needs**
   - Can the code be isolated with mocks? → unit test
   - Does it need real dependencies to work correctly? → integration test
   - Does it need full system context? → e2e test

3. **Evaluate testing goals**
   - Fast feedback on logic changes → unit test
   - Verify integration works → integration test
   - Validate user experience → e2e test
   - Ensure API compatibility → contract test

4. **Apply Python-specific considerations**
   - Async code: unit tests with asyncio mock, integration with real async services
   - Django/Flask/FastAPI: use test clients for integration, mocks for unit
   - Database: use pytest fixtures with in-memory or test DB
   - Filesystem: use pytest tmp_path fixture

5. **Consider test pyramid**
   - Many unit tests (fast, cheap)
   - Fewer integration tests (medium speed, medium cost)
   - Minimal e2e tests (slow, expensive)
   - Contract tests where services are independent

## Test Level Guidelines

| Test Level | When to Use | Python Tools | Speed |
|------------|-------------|--------------|-------|
| **Unit** | Pure logic, business rules, no external deps | unittest.mock, pytest-mock | Fastest |
| **Integration** | Module boundaries, DB, API, filesystem | pytest fixtures, testcontainers | Medium |
| **E2E** | User workflows, full system paths | pytest + selenium/playwright | Slowest |
| **Contract** | API compatibility, service interfaces | pytest + pact/contract libraries | Fast |

## Guardrails

- Don't use unit tests for code that requires real dependencies to work
- Don't use e2e tests for logic that can be tested faster with unit tests
- Avoid "integration tests" that are actually unit tests with one mock removed
- Don't create test levels just for the sake of having them

## Example prompts

```
What test level should I use for this function?

```python
def calculate_discount(price: float, user: User, items: list[Item]) -> float:
    # Pure calculation logic
    pass
```

---

Determine the appropriate test level for this code:

```python
async def sync_inventory():
    # Fetches from external API, updates database, sends notifications
    pass
```

---

What test level is appropriate for these scenarios in my Flask app?

1. Validating request schema parsing
2. Testing database query generation
3. Verifying full user registration flow
4. Ensuring API response format matches spec
