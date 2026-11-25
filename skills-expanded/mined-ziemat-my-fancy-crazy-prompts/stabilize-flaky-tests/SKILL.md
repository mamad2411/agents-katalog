name: stabilize-flaky-tests
description: Improves determinism, isolation, timing control, fixture hygiene, and environmental reliability in Python tests. Use this when you need to fix flaky tests that fail intermittently.

---

# Stabilize Flaky Tests

## Purpose

Improve determinism, isolation, timing control, fixture hygiene, and environmental reliability in Python tests. This skill fixes flaky tests that fail intermittently by addressing timing issues, state leakage, and environmental dependencies.

## Use when

- A test is failing intermittently (flaky)
- Tests pass locally but fail in CI
- Test results vary between runs
- Tests depend on timing or external state
- Investigating CI failures that are hard to reproduce

## Do not use when

- A test is consistently failing (use `fix-failing-tests`)
- You need to write new tests
- The flakiness is due to an external system outage

## Inputs

- Flaky test code
- Failure history or patterns
- CI logs or error messages
- Test execution environment details

## Outputs

- Root cause analysis for flakiness
- Specific fixes for each issue
- Improved test code with stability fixes
- Recommendations for preventing future flakiness

## Method

1. **Identify flakiness patterns**
   - When does it fail? (CI, specific times, after certain tests)
   - What's the error message?
   - Is there a pattern in failures?
   - Can you reproduce it consistently?

2. **Check for timing issues**
   - Async code without proper await
   - Race conditions in concurrent code
   - Time-dependent logic (datetime.now(), sleep)
   - External calls with variable latency

3. **Verify fixture hygiene**
   - Are fixtures properly isolated?
   - Is state cleaned up after tests?
   - Are mutable defaults avoided?
   - Is test order dependency eliminated?

4. **Review environmental dependencies**
   - Are external services mocked properly?
   - Is test data isolated?
   - Are environment variables set correctly?
   - Is filesystem state managed?

5. **Apply stability fixes**
   - Use proper async patterns
   - Add retries with backoff for external calls
   - Use fixtures with proper scope and cleanup
   - Replace time-dependent logic with injectable time

## Common Flakiness Fixes

| Issue | Fix |
|-------|-----|
| **Async race conditions** | Use `asyncio.sleep()` instead of `time.sleep()`, proper `await` |
| **Fixture state leakage** | Use `scope="function"`, clean up in `yield` fixtures |
| **Time-dependent tests** | Inject `time` dependency, use `freezegun` |
| **External service calls** | Mock with `responses`, `httpretty`, or test containers |
| **Filesystem race conditions** | Use `tmp_path` fixture, unique filenames |
| **Database state leakage** | Use transaction rollback, unique test data |

## Guardrails

- Don't add `time.sleep()` to "fix" flakiness; fix the root cause
- Don't make tests slower than necessary
- Don't remove assertions to make tests pass
- Make sure fixes don't hide real issues

## Example prompts

```
Stabilize this flaky test:

```python
def test_async_processing():
    result = async_process()
    time.sleep(0.1)  # Magic number
    assert result.status == "completed"

# Fails intermittently when processing takes > 0.1s
```

---

Fix this flaky test with fixture issues:

```python
@pytest.fixture
def db_session():
    return get_test_db()  # Shared state, not cleaned up

def test_user_creation(db_session):
    db_session.add(User(name="test"))
    # No cleanup, affects other tests

def test_user_query(db_session):
    # Fails if previous test didn't clean up
    assert db_session.query(User).count() == 1
```

---

Stabilize this CI-flaky test:

```python
def test_api_call():
    response = requests.get("https://api.example.com/data")
    assert response.status_code == 200

# Works locally, fails in CI (network issues, rate limits)
```
