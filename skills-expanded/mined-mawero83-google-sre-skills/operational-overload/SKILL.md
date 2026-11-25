---
name: operational-overload
description: >-
  Detect and recover from operational overload: interrupts, paging load, and embedding SRE to recover — from Google SRE. Use when a team is drowning.
---

# Operational Overload

**Domain:** `organization`  
**Sources:** Workbook Ch17, SRE Book 1e Ch29–30

## When to use

- Team interrupt load unsustainable
- Toil and pages crush project work
- Rescue engagement requested

## Principles

- Overload hides problems and creates more incidents.
- Measure interrupts; set explicit reclaim plan.
- Temporarily reduce scope / freeze features if needed to recover.
- Embedding help should transfer capability, not create dependency forever.

## Workflow

1. Quantify pages, tickets, after-hours, project time.
2. Declare overload; agree recovery window with leadership.
3. Cut noise; defer noncritical work; automate top toil.
4. Staff recovery; set exit criteria for helpers.
5. Reassess in 4–6 weeks with numbers.

## Decision guide

- If leadership refuses scope cut → document risk; escalate.

## Output template

```markdown
# Overload recovery plan
- Metrics now:
- Scope cuts:
- Noise/toil actions:
- Help embedded:
- Exit criteria:
```

## Anti-patterns

- Heroics as strategy.
- Help that never leaves.

## Related skills

`alert-noise-reduction`, `eliminating-toil`, `on-call-excellence`

## Canonical references

- [Recovering from Overload](https://sre.google/workbook/recovering-from-overload/)
- [Dealing with Interrupts](https://sre.google/sre-book/dealing-with-interrupts/)
- [Embedding SRE to Recover](https://sre.google/sre-book/operational-overload/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
