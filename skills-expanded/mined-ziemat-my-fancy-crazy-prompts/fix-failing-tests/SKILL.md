name: fix-failing-tests
description: Determines whether Python test failures come from product bugs, outdated expectations, or test design issues. Use this when a test is failing and you need to diagnose the root cause.

---

# Fix Failing Tests

## Purpose

Determine whether Python test failures come from product bugs, outdated expectations, or test design issues. This skill diagnoses the root cause of test failures and recommends the appropriate fix.

## Use when

- A test is failing and you need to understand why
- Investigating test failures in CI/CD
- Deciding whether to fix the code or the test
- Debugging intermittent test failures
- Reviewing test failures after a code change

## Do not use when

- You need to write the actual fix (use `generate-unit-tests` or `generate-integration-tests`)
- You're debugging a production issue (focus on the code, not the test)
- You need to stabilize flaky tests (use `stabilize-flaky-tests`)

## Inputs

- Failing test code
- Error message or traceback
- Related code changes
- Test history or recent commits

## Outputs

- Diagnosis of the failure cause (bug, outdated test, design issue)
- Recommended fix for each cause
- Priority ranking of fixes
- Steps to verify the fix

## Method

1. **Analyze the failure**
   - Read the error message and traceback
   - Identify what assertion failed
   - Note the expected vs actual values
   - Check if the failure is consistent

2. **Determine failure category**
   - **Product bug**: Code changed, test is correct, behavior is wrong
   - **Outdated test**: Test expectations don't match new (correct) behavior
   - **Test design issue**: Test is fragile, flaky, or incorrectly written

3. **Verify the diagnosis**
   - Check if the code change was intentional
   - Review the test's purpose and assertions
   - Consider if the test is testing the right thing
   - Check for timing or isolation issues

4. **Recommend fixes**
   - For product bugs: Fix the code, keep the test
   - For outdated tests: Update the test expectations
   - For design issues: Refactor the test

5. **Verify the fix**
   - Run the test after the fix
   - Ensure no other tests broke
   - Confirm the fix addresses the root cause

## Failure Categories

| Category | Signs | Fix |
|----------|-------|-----|
| **Product bug** | Test was passing, code changed, behavior is wrong | Fix the code |
| **Outdated test** | Test expectations don't match new behavior | Update test |
| **Test design** | Test is flaky, timing-dependent, over-specified | Refactor test |
| **Environment** | Test works locally but fails in CI | Fix environment setup |

## Guardrails

- Don't assume the test is wrong just because it's failing
- Don't ignore test failures; always investigate
- Consider whether the code change was intentional
- Make sure the fix addresses the root cause, not just the symptom

## Example prompts

```
Diagnose this failing test:

```python
def test_calculate_total():
    order = Order(items=[{"price": 100}, {"price": 50}])
    assert order.total() == 150.0

# Error: AssertionError: assert 165.0 == 150.0
# Code change: Added 10% tax calculation
```

---

What's causing this test failure?

```python
async def test_api_response():
    response = await api.get("/users")
    assert response.status_code == 200
    assert response.json() == {"users": []}

# Error: AssertionError: assert {'users': []} == {'users': []}
# Code change: Changed response format from {"users": []} to {"data": {"users": []}}
```

---

Diagnose this flaky test:

```python
def test_concurrent_updates():
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(update, items))
    assert len(results) == len(items)

# Error: Sometimes passes, sometimes fails with AssertionError
```
