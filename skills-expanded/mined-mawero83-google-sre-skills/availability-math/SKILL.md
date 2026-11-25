---
name: availability-math
description: >-
  Use availability math tactically: nines tables, downtime budgets, and error-budget arithmetic for planning and communication. Use when converting SLOs to allowed downtime/failure counts.
---

# Availability Math

**Domain:** `foundations`  
**Sources:** SRE Book 1e App A, Workbook Ch2

## When to use

- Explaining what 99.9% means in minutes
- Computing allowed errors from traffic
- Comparing SLO options

## Principles

- Nines map to concrete downtime; use tables, do not guess.
- Budget in events is often clearer than abstract percentages.
- Window choice (28d/30d/quarter) changes operational behavior.

## Workflow

1. Pick SLO % and window.
2. Convert to allowed downtime and/or bad events given traffic.
3. Show what a single incident consumes as % of budget.
4. Use in policy and alert design conversations.

## Decision guide

- If stakeholders argue nines without minutes → show the table.

## Output template

```markdown
# Budget arithmetic
- SLO / window:
- Allowed downtime:
- Expected events:
- Allowed bad events:
- Example incident cost:
```

## Anti-patterns

- Marketing five-nines without budget math.

## Quick reference (approx downtime / month)

| Availability | Downtime / month |
|--------------|------------------|
| 99% | ~7.3 h |
| 99.9% | ~43.8 m |
| 99.99% | ~4.4 m |
| 99.999% | ~26 s |


## Related skills

`sli-slo-design`, `error-budget-policy`, `alerting-on-slos`

## Canonical references

- [Availability Table](https://sre.google/sre-book/availability-table/)
- [Implementing SLOs](https://sre.google/workbook/implementing-slos/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
