---
name: tdd
description: Test-Driven Development with built-in completion gate — write failing test, watch it fail, write minimal code to pass, verify with evidence before claiming success
---

# tdd

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over. No exceptions.

## Red-Green-Refactor

**Red:** Write a failing test. Verify it fails for the right reason (feature missing, not a typo). One behavior, clear name, real code (no mocks unless unavoidable).

**Green:** Write the simplest code to pass the test. Do not add features, refactor nearby code, or "improve" beyond what the test requires.

**Refactor:** Clean up after green only. Remove duplication, improve names, extract helpers. Keep tests green. Don't add behavior.

**Repeat** with the next failing test for the next feature.

## Good test vs bad test

**Good:**
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => { attempts++; if (attempts < 3) throw new Error('fail'); return 'success'; };
  const result = await retryOperation(operation);
  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
Clear name, tests real behavior, one thing.

**Bad:**
```typescript
test('retry works', async () => {
  const mock = jest.fn().mockRejectedValueOnce(new Error()).mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
Vague name, tests mock not code.

## Example: Bug Fix

**Bug:** Empty email accepted

```typescript
// RED: Write failing test
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});

// Verify RED: run test, confirm FAIL with "expected 'Email required', got undefined"

// GREEN: Minimal implementation
function submitForm(data) {
  if (!data.email?.trim()) return { error: 'Email required' };
  // ...
}

// Verify GREEN: run test, confirm PASS
```

## Common rationalizations — stop

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests after pass immediately — proves nothing. |
| "Tests after achieve same goals" | Tests-first: "what SHOULD this do?" Tests-after: "what DOES this do?" |
| "Already manually tested" | Manual is ad-hoc. Can't re-run. No record. |
| "Deleting hours of work is wasteful" | Sunk cost. Untested code is technical debt. |
| "Test hard = design unclear" | Listen: hard to test = hard to use. Simplify. |

## When stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the wished-for API first. Assertion first. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. |

## Verification checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for the expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass, output pristine (no warnings)
- [ ] Tests use real code (mocks only if unavoidable)

Can't check all boxes? You skipped TDD. Start over.

## Completion Gate

**Before claiming completion or moving to the next task:**

1. **Identify:** what command proves the work is done? (test suite, build, `git diff`)
2. **Run:** execute it now, in this message.
3. **Read:** check full output, count failures, confirm exit code.
4. **Verify:** does output confirm the claim?
   - If NO: state actual status with evidence. Do not claim success.
   - If YES: state claim WITH the evidence.

| Claim | Requires |
|-------|---------|
| Tests pass | Test command output: 0 failures |
| Build succeeds | Build command: exit 0 |
| Bug fixed | Test for original symptom: passes |
| Agent completed | Check VCS diff — verify changes exist |

**Escalation context:** If invoked because a Quick-tier task failed its completion gate, invoke `Skill(imlazy-learn)` to record the misclassification (predicted=quick, actual=standard, task summary ≤50 chars) before proceeding. Then continue with TDD on the task — do not redo work already done correctly in the Quick attempt.
