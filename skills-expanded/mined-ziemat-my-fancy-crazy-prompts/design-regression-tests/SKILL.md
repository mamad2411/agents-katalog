name: design-regression-tests
description: Designs Python tests that specifically prevent previously seen or likely regressions. Use this when you need to create tests that catch bugs from past incidents or prevent common regression patterns.

---

# Design Regression Tests

## Purpose

Design Python tests that specifically prevent previously seen or likely regressions. This skill creates targeted tests that catch bugs from past incidents and prevent common regression patterns from recurring.

## Use when

- Creating tests after fixing a bug
- Building a regression test suite
- Responding to production incidents
- Planning tests for a refactor or migration
- Adding tests to prevent known failure modes

## Do not use when

- You're writing initial tests for new functionality (use `generate-unit-tests`)
- You need to design a comprehensive test strategy (use `design-high-value-tests`)
- You're debugging a specific failure

## Inputs

- Bug report or incident description
- Fixed code or proposed changes
- Previous test suite (if available)
- Error logs or reproduction steps

## Outputs

- Regression test cases with clear reproduction steps
- Test assertions that would have caught the original bug
- Expected behavior vs buggy behavior
- Integration points for the regression tests

## Method

1. **Understand the failure**
   - What was the expected behavior?
   - What was the actual buggy behavior?
   - What conditions triggered the bug?
   - What was the impact of the bug?

2. **Create minimal reproduction**
   - Strip away unrelated code
   - Focus on the specific failure scenario
   - Make the test fail before the fix, pass after

3. **Design effective assertions**
   - Assert on the actual bug manifestation
   - Include assertions that would have caught it earlier
   - Avoid over-specifying implementation details

4. **Consider related regressions**
   - What similar code paths could have the same bug?
   - What edge cases might also be affected?
   - What assumptions did the bug violate?

5. **Integrate into test suite**
   - Choose appropriate test level
   - Name the test to describe the bug scenario
   - Add to relevant test file or suite
   - Consider adding to CI if not already covered

## Regression Test Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Exact reproduction** | Bug was triggered by specific input | Test with the exact failing input |
| **Generalized variant** | Bug could occur with similar inputs | Test with related edge cases |
| **Behavior preservation** | Refactoring could break existing behavior | Test the behavior that was working |
| **Error handling** | Bug was in exception handling | Test the error path explicitly |

## Guardrails

- Don't just test the exact bug; test the underlying assumption that was violated
- Don't write tests that only pass because of the specific fix
- Avoid testing implementation details that could change
- Make sure the test would fail if the bug returns

## Example prompts

```
Design a regression test for this bug fix:

Bug: User login failed when email contained uppercase letters
Fix: Added `.lower()` to email normalization
Code:
```python
def authenticate(email: str, password: str) -> User | None:
    user = db.find_user(email)  # Was case-sensitive
    if user and verify_password(password, user.hash):
        return user
```

---

Create regression tests for this incident:

Incident: Payment processing failed for amounts with 3 decimal places
Root cause: Amount was parsed as int instead of float
Fix: Changed parsing logic to use Decimal

---

Design regression tests for this refactoring:

Before:
```python
def process_order(order):
    if order.total > 100:
        return apply_discount(order, 0.1)
    elif order.total > 50:
        return apply_discount(order, 0.05)
    return order
```

After:
```python
def process_order(order):
    tier = get_discount_tier(order.total)
    return apply_discount(order, tier)
```

Known issue: The old code had a bug where total == 50 didn't get any discount
