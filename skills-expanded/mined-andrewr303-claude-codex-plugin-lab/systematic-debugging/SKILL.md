---
name: systematic-debugging
description: Use for bugs, failing tests, crashes, incorrect behavior, flaky workflows, or confusing error reports.
---

# Systematic Debugging

Do not patch symptoms before locating the first divergence.

## Steps

1. Pin expected behavior, actual behavior, exact error, inputs, environment, and recent changes.
2. Name at least two plausible causes.
3. For each cause, name the check that would falsify it.
4. Reproduce or create the closest available reproduction.
5. Trace where state first diverges.
6. Fix at the originating layer.
7. Verify the original failing case.
8. Search for the same bug class elsewhere.

## AI/Agentic Systems

Separate layers before blaming the model:

- prompt/input
- retrieval/source freshness
- output schema
- parser/validator
- tool dispatch
- memory/state
- downstream logic
- UI cache
- permission state

## Handoff Shape

```md
Root cause:
Fix:
Verification:
Blast radius checked:
Remaining uncertainty:
```

