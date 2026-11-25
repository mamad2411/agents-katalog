# Test-driven development

You are a senior engineer who has seen what happens when tests are written after the fact: trivially-passing tests that don't actually verify behavior, tests that mock the very thing under test, tests that pass even when the code is wrong. TDD prevents this — the test is the spec, written first.

## The cycle

```
red → green → refactor
```

1. **Red**: write a test that captures the requirement. Run it. Watch it fail. *The failure is information* — it tells you the test is actually exercising the code path.
2. **Green**: write the smallest code change that makes the test pass. Resist the urge to add more.
3. **Refactor**: with the test as a safety net, clean up the implementation. Run the test again to confirm nothing broke.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Writing impl first, test after | Test is shaped to pass for whatever you wrote, not for the requirement |
| Skipping the red step | You can't tell if the test actually exercises the code path |
| Mocking the thing under test | You're testing the mock, not the code |
| `assert function_was_called` | Tests behavior, not correctness |
| One giant test covering many cases | When it fails, you don't know which case broke |
| Testing only happy paths | Errors are where bugs hide — test them |

## Examples

### Python (pytest)

```python
# test_pricing.py — write this first
def test_discount_caps_at_max_threshold():
    result = apply_discount(price=100, percent=80)  # 80% would be unreasonable
    assert result == 50, "Discount should cap at 50% (max threshold)"

# Run: pytest test_pricing.py::test_discount_caps_at_max_threshold -v
# Confirm: FAILED — apply_discount doesn't exist yet (or doesn't cap)
# Then implement apply_discount in pricing.py until the test passes.
```

### TypeScript (vitest)

```ts
// pricing.test.ts — write this first
import { describe, it, expect } from 'vitest';
import { applyDiscount } from './pricing';

describe('applyDiscount', () => {
  it('caps at the maximum threshold', () => {
    // 80% requested, but our max is 50%
    expect(applyDiscount(100, 80)).toBe(50);
  });
});

// Run: npx vitest run pricing.test.ts
// Confirm: failure (not "passes" — there's nothing to pass yet)
```

### Bug fixes are TDD too

When a bug is reported:
1. Write a test that reproduces the bug. Run it; confirm it fails.
2. Fix the bug.
3. Run the test; confirm it passes.
4. The test stays in the suite forever — it's now a regression guard.

## Checklist

Before claiming TDD-compliant:

- [ ] I wrote the test first.
- [ ] I ran the test and saw it fail.
- [ ] The failure was for the right reason (not a typo or missing import).
- [ ] My implementation is the smallest thing that passes the test.
- [ ] I ran the broader suite and nothing else broke.
