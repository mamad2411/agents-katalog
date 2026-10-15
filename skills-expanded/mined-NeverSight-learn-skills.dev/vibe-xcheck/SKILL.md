---
name: vibe-xcheck
description: Build and run post-change verification covering positive, boundary, negative, regression, and sanity checks.
---

# vibe-xcheck

Use this skill after EXEC and before COMPLETE.

## Required coverage

- Positive minimal path
- Boundary input
- Negative input
- Regression path
- Affected module sanity check
- Performance or size sanity check when relevant

## Output

Record:

```text
Commands run:
Scenarios covered:
Result:
Known gaps:
```

If checks fail, return to REVIEW/EXEC.
