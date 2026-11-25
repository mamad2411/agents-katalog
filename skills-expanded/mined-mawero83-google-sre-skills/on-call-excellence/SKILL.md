---
name: on-call-excellence
description: >-
  Design healthy on-call: load targets, escalation, handoffs, compensation of cognitive load, and sustainable rotations per Google SRE. Use when creating schedules, fixing burnout, or reviewing on-call health.
---

# On Call Excellence

**Domain:** `operations`  
**Sources:** SRE Book 1e Ch11, Workbook Ch8, SRE Book 2e Ch10

## When to use

- Building or fixing an on-call rotation
- Burnout / too many pages
- Handoff quality problems

## Principles

- On-call must be sustainable; paging load is a first-class SLO for the team.
- Clear escalation, ownership, and compensatory time/pay matter.
- Handoffs need written state, not tribal knowledge.
- Secondary/escalation exists to bound primary load.

## Workflow

1. Measure pages/shift, night pages, MTTA, interrupted sleep.
2. Set a target load and alert noise budget.
3. Ensure runbooks linked from every page.
4. Define escalation tree and incident commander path.
5. Standardize handoff template (see docs/templates/).
6. Review monthly: tune alerts, not heroes.

## Decision guide

- If nights are brutal → fix noise before adding people.
- If follow-the-sun → explicit timezone ownership of services.

## Output template

```markdown
# On-call health review
- Rotation + coverage model:
- Pages/shift (28d):
- Top noisy alerts:
- Handoff quality:
- Actions:
```

## Anti-patterns

- Badge of honor for suffering.
- Unpaid endless secondary.

## Related skills

`alert-noise-reduction`, `incident-management`, `operational-overload`

## Canonical references

- [Being On-Call](https://sre.google/sre-book/being-on-call/)
- [Workbook On-Call](https://sre.google/workbook/on-call/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
