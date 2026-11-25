---
name: outage-tracking
description: >-
  Track outages for trends: taxonomy, budget impact, and planning inputs per Google SRE. Use for reliability reporting and quarterly planning.
---

# Outage Tracking

**Domain:** `operations`  
**Sources:** SRE Book 1e Ch16, Workbook App C

## When to use

- Building outage database / scorecards
- Quarterly reliability review

## Principles

- What gets tracked gets improved — with care to avoid vanity metrics.
- Tag by cause class, detection, mitigation, CUJ, budget burn.
- Use trends to fund reliability themes, not blame teams.

## Workflow

1. Define mandatory outage record fields.
2. Ensure every Sev/postmortem feeds the tracker.
3. Monthly rollup: top classes, MTT* , budget consumers.
4. Feed top classes into planning as P0 themes.

## Decision guide

- If scorecards are gamed → shift to outcome SLOs + learning quality.

## Output template

```markdown
# Outage rollup
- Window:
- Count by severity/class:
- Worst budget burns:
- Themes for planning:
```

## Anti-patterns

- Weaponized scorecards without context.

## Related skills

`learning-from-incidents`, `error-budget-policy`, `production-meetings`

## Canonical references

- [Tracking Outages](https://sre.google/sre-book/tracking-outages/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
