---
name: cascading-failures
description: >-
  Detect and break cascading failures: latency death spirals, retry storms, shared fate, and recovery strategies from Google SRE. Use during incidents with amplifying failure or design reviews for cascade risk.
---

# Cascading Failures

**Domain:** `resilience`  
**Sources:** SRE Book 1e Ch22, SRE Book 2e Ch17

## When to use

- Failure spreading across services
- Latency amplifying errors
- Designing bulkheads

## Principles

- Cascades often come from retries, shared threads, coupled timeouts, and synchronized behavior.
- Break feedback loops: shed, isolate, reduce fanout, freeze bad deploys.
- Recover deliberately — thundering herds on recovery are common.
- Test partial dependency failure, not only total death.

## Workflow

1. Draw amplifying loops (retry → latency → timeout → retry).
2. Insert bulkheads: pools, limits, circuit breakers, caches.
3. Align timeouts decreasing toward the edge or with explicit budgets.
4. Add load-shed and degrade modes for noncritical paths.
5. Plan recovery pacing (warmup, token release).

## Decision guide

- If one bad canary poisoned peers via shared state → improve isolation.

## Output template

```markdown
# Cascade risk review
- Amplifying loops:
- Bulkheads present/missing:
- Timeout/retry map:
- Recovery plan:
```

## Anti-patterns

- More retries as the only fix.
- Shared everything clusters.

## Related skills

`handling-overload`, `designing-for-resilience`, `effective-troubleshooting`

## Canonical references

- [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
