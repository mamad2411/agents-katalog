---
name: organizational-change
description: >-
  Drive organizational change for SRE adoption: stakeholders, incremental change, and resistance handling from the SRE Workbook. Use for transformations and reliability programs.
---

# Organizational Change

**Domain:** `organization`  
**Sources:** Workbook Ch21, SRE Book 2e Ch4/6

## When to use

- Company-wide SRE adoption
- Resistance to error budgets
- Changing on-call or launch process

## Principles

- Change is a process with sponsors, early wins, and communication.
- Start where pain is acknowledged.
- Codify wins into policy/platform so they survive reorgs.

## Workflow

1. Map stakeholders and objections.
2. Pick a pilot with visible pain and willing partners.
3. Deliver measurable win (noise↓ or budget clarity).
4. Broadcast; expand; institutionalize.

## Decision guide

- If no executive sponsor → limit ambition; build evidence first.

## Output template

```markdown
# Change plan
- Sponsor:
- Pilot:
- Success metric:
- Expand criteria:
```

## Anti-patterns

- Big-bang reorg without pilot.
- Policy without enablement.

## Related skills

`sre-culture`, `sre-org-structures`, `error-budget-policy`

## Canonical references

- [Organizational Change Management](https://sre.google/workbook/organizational-change/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
