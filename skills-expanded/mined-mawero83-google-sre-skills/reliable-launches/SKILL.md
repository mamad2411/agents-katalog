---
name: reliable-launches
description: >-
  Run reliable product launches at scale using Google launch coordination practices: checklists, capacity, flags, and criteria. Use for big launches and production readiness style gates.
---

# Reliable Launches

**Domain:** `delivery`  
**Sources:** SRE Book 1e Ch27 + App E, SRE Book 2e Ch7/20 themes

## When to use

- Major feature/product launch
- Production readiness review
- Launch checklist design

## Principles

- Launches fail from capacity, config, dependency, and ops unreadiness more than 'code bugs' alone.
- Checklist + named owners beat tribal hope.
- Feature flags and staged exposure are default.
- Abort criteria agreed before launch day.

## Workflow

1. Draft launch checklist from CUJs, deps, capacity, SLOs, runbooks, paging.
2. Run PRR-style review; track gaps to owners.
3. Dry-run monitoring/alerts and rollback.
4. Launch with staged traffic; watch burn and business KPIs.
5. Post-launch review within a week.

## Decision guide

- If SLO/alerting missing → no go for user-critical launches.

## Output template

```markdown
# Launch readiness
- Checklist status:
- Blockers:
- Stage plan:
- Abort criteria:
- On-call coverage:
```

## Anti-patterns

- Launch without rollback.
- Pager setup on launch day.

## Related skills

`canarying-releases`, `capacity-planning`, `sli-slo-design`

## Canonical references

- [Reliable Product Launches](https://sre.google/sre-book/reliable-product-launches/)
- [Launch Checklist](https://sre.google/sre-book/launch-checklist/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
