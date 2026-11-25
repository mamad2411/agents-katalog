---
name: structural-implementing
description: Use when implementing non-trivial code paths, endpoint handlers, jobs, workflows, migrations, parsers, retries, resource lifecycles, tests, or behavior changes.
---

# Structural Implementing

Turn the plan into code whose safe path is the natural path.

Core rule:

> Make the illegal state unrepresentable, the hostile input bounded, the mutation replay-safe, and the failure impossible to swallow.

## Default output

```md
## Boundary shape
- Parsed input:
- Trust/auth/size bounds:
- Domain state representation:

## Runtime safety
- Deadlines / cancellation:
- Resource ownership / teardown:
- Atomicity / idempotency:

## Operability
- Failure visibility:
- Signals:
- Tests written while building:
```

## Implementation checks

- Re-check load-bearing plan assumptions against the current code before building.
- Parse at the door into a narrower type or schema-checked value. Carry the parsed form inward.
- Keep reasoning local. Avoid globals, hidden mutation, call-order dependencies, and action-at-a-distance.
- Give every ambient dependency one seam: clock, random, environment, HTTP client, filesystem, queue.
- Use names that reveal units, ordering, side effects, freshness, and idempotency when types cannot.
- Keep responsive paths free of uncontrolled-latency work; put deadlines on cross-boundary waits.
- Bound caller-controlled growth and release every acquired resource on every exit path.
- Fix caller-controlled super-linear cost and N+1/chatty calls on sight; measure before other optimisations.
- Make shared-state mutation atomic/serialised and retried operations idempotent.
- Make failure visible in the language idiom; never swallow silently.
- Emit the signal while writing the code.
- Test contracts, parsers, decisions, failures, replay, and seams as you build.

## Red flags

- Raw DTOs or unvalidated strings reaching core logic.
- `Date.now()`, randomness, env, or clients buried where tests cannot override them.
- `SELECT` then `INSERT`, “processing” flags, or duplicate-click-sensitive mutations.
- Unbounded retries, queues, buffers, recursion, fan-out, or file uploads.
- Empty catches, ignored errors, unhandled rejections, or success-only telemetry.
