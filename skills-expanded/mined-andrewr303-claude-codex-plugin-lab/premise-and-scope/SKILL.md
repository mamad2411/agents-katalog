---
name: premise-and-scope
description: Use when the task may be misframed, underspecified, overbroad, risky, or based on an unverified assumption.
---

# Premise And Scope

This skill prevents confident work on the wrong problem.

## Process

1. Extract the user's desired outcome and the typed request separately.
2. List the embedded premises that must be true.
3. Mark each premise:
   - `verified`: directly observed this session.
   - `inferred`: follows from observed facts.
   - `assumed`: not yet established.
4. Run the cheapest check that could kill the plan.
5. If the premise survives, continue to `design-brief` or `implementation-planning`.
6. If the premise fails, offer the corrected path and stop before editing.

## Checks

- Open actual files, configs, schemas, routes, tests, or logs.
- For current external facts, read primary sources.
- For UI claims, inspect the rendered surface or screenshots when available.
- For performance claims, measure before optimizing.

## Output

Use this compact shape:

```md
Need:
Premises:
- verified:
- inferred:
- assumed:
Killer check:
Decision:
Next:
```

