---
name: test-harness
description: >
  Reusable method for selecting and interpreting verification. Use when deciding
  which tests to run, diagnosing failures, or separating regressions from
  harness drift.
---

# Test Harness Skill

Use this when the central question is verification.

## Method

1. Identify the behavior boundary.
2. Choose the smallest falsifying check.
3. Run focused checks before broad suites.
4. Attribute failures before fixing anything.
5. Report skipped checks plainly.
6. Recommend broader validation only when risk justifies it.

## Failure Categories

- product behavior regression;
- test expectation drift;
- missing dependency or environment setup;
- stale path or fixture assumption;
- unrelated pre-existing failure.

## Output

```text
Behavior boundary:
Commands run:
Result:
Failure attribution:
Confidence:
Recommended next check:
Lesson candidate:
```
