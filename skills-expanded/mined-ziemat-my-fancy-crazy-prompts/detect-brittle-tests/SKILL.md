name: detect-brittle-tests
description: Finds Python tests that are fragile, overspecified, timing-sensitive, or coupled to internals. Use this when you need to identify tests that are likely to fail unnecessarily or require frequent maintenance.

---

# Detect Brittle Tests

## Purpose

Find Python tests that are fragile, overspecified, timing-sensitive, or coupled to internals. This skill identifies tests that are likely to fail unnecessarily or require frequent maintenance, helping improve test suite reliability.

## Use when

- Reviewing test suite quality
- Investigating flaky test failures
- Refactoring code and tests are breaking
- Maintaining a large test suite
- Preparing for a major refactor

## Do not use when

- You need to fix the actual test code (use `fix-failing-tests` or `stabilize-flaky-tests`)
- You're writing new tests
- You need to identify what functionality is missing

## Inputs

- Python test files
- Test failure history or flakiness data
- Code changes or refactoring plans
- Test execution timing data (optional)

## Outputs

- List of brittle tests with specific issues
- Risk assessment for each test
- Recommendations for improvement
- Priority ranking for fixes

## Method

1. **Identify common brittleness patterns**
   - Tests that check implementation details
   - Tests with hardcoded values or strings
   - Tests with timing dependencies
   - Tests with fragile assertions

2. **Check for over-specification**
   - Asserting on exact return values when behavior is what matters
   - Checking internal state instead of public API
   - Verifying call order instead of outcomes
   - Testing private methods directly

3. **Find timing dependencies**
   - Tests using `time.sleep()`
   - Async tests without proper await
   - Tests depending on system time
   - Race conditions in concurrent tests

4. **Identify coupling to internals**
   - Tests that break with refactoring
   - Tests checking exception messages exactly
   - Tests depending on error order
   - Tests using specific class attributes

5. **Assess test isolation**
   - Tests that depend on global state
   - Tests that don't clean up after themselves
   - Tests that share mutable fixtures
   - Tests that depend on execution order

## Brittle Test Indicators

| Indicator | Example | Fix |
|-----------|---------|-----|
| **Exact string match** | `assert error_msg == "User not found"` | `assert "not found" in error_msg.lower()` |
| **Internal state check** | `assert obj._cache == {...}` | Test via public API |
| **Timing dependency** | `time.sleep(1); assert result` | Use proper async/await |
| **Call order assertion** | `mock.method.assert_called_once_with(...)` | Assert outcome instead |
| **Global state** | `os.environ["KEY"] = "value"` | Use `monkeypatch` fixture |

## Guardrails

- Don't flag tests that need to check implementation for correctness
- Consider whether the brittleness is acceptable for the test's purpose
- Balance test stability with test value
- Don't remove tests that catch real bugs, even if brittle

## Example prompts

```
Identify brittle tests in this test file:

```python
def test_process_order():
    order = Order()
    order.items = [{"price": 100}]
    result = order.process()
    assert result.status == "completed"  # Exact string
    assert result.total == 100.0  # Float comparison
    assert order._cache["processed"] == True  # Internal state
```

---

Find brittle tests in this async test suite:

```python
@pytest.mark.asyncio
async def test_api_call():
    result = await api.call()
    time.sleep(0.1)  # Magic number
    assert result == {"status": "ok"}  # Exact structure
```

---

Which tests are likely to break with refactoring?

```python
def test_user_creation():
    user = User(first_name="John", last_name="Doe")
    assert user.full_name == "John Doe"
    assert user._id is not None  # Internal attribute
    assert len(user._permissions) == 0  # Internal list
```
