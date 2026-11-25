---
name: handling-overload
description: >-
  Prevent and handle overload: load shedding, throttling, queue management, and graceful degradation per Google SRE. Use when systems melt under traffic or retries, or designing anti-overload controls.
---

# Handling Overload

**Domain:** `resilience`  
**Sources:** SRE Book 1e Ch21, SRE Book 2e Ch15/17, Workbook Ch11

## When to use

- Traffic storms / retry storms
- Designing rate limits / shedding
- Queue depth explosions

## Principles

- Overload is inevitable; design explicit degraded modes.
- Shed cheapest discardable work first; protect critical CUJs.
- Server and client controls both matter; clients must back off.
- Queues without bounds become latency weapons.

## Workflow

1. Identify critical vs shedable work.
2. Set concurrency/queue limits with visible metrics.
3. Implement prioritized shedding + user-visible degrade.
4. Add client retry budgets and exponential backoff + jitter.
5. Load test past expected peaks; verify recoverable collapse.

## Decision guide

- If returning 200 on failure to 'be nice' → stop; fail clearly.
- If global lock/queue → partition or shed.

## Output template

```markdown
# Overload control plan
- Critical CUJs:
- Shed order:
- Limits (concurrency/QPS/queue):
- Client backoff policy:
- Test evidence:
```

## Anti-patterns

- Unbounded queues.
- Synchronized retries.

## Related skills

`cascading-failures`, `load-management`, `capacity-planning`

## Canonical references

- [Handling Overload](https://sre.google/sre-book/handling-overload/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
