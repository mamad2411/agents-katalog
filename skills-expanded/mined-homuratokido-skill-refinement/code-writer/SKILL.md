---
name: code-writer
description: >
  Reusable method for bounded implementation with self-verification. Use when
  the task has clear ownership, a concrete spec, and a checkable outcome.
---

# Code Writer Skill

Use this for small patches, tests, dependency fixes, or focused documentation
changes.

## Method

1. State spec, ownership, forbidden files, and verification target.
2. Read the smallest necessary source and test slices.
3. Make the minimal change that satisfies the spec.
4. Run the closest relevant check first.
5. Attribute failures before changing more code.
6. Report the diff scope and residual risk.

## Avoid

- Expanding scope because adjacent code looks messy.
- Committing from a worker context.
- Treating static checks as a substitute for behavior tests when behavior tests
  exist.

## Output

```text
Spec:
Files changed:
Validation:
Failures handled:
Residual risk:
Lesson candidate:
```
