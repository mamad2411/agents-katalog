---
name: sre-org-structures
description: >-
  Choose SRE organizational structures: centralized, embedded, hybrid, and maturity models from SRE Book 2e. Use when designing or reorging SRE.
---

# SRE Org Structures

**Domain:** `organization`  
**Sources:** SRE Book 2e Ch6, Workbook Ch20

## When to use

- Reorg / creating SRE org
- Choosing embedded vs central platform SRE
- Maturity assessment

## Principles

- Structure follows engagement intent and scale.
- Hybrid models often win: platform core + embedded reliability partners.
- Maturity matrices help; vanity scorecards harm.
- On-call design must match structure.

## Workflow

1. Clarify goals: platform leverage vs product depth.
2. Pick structure; define interfaces and ownership of paging.
3. Pilot; measure outcomes (SLO health, toil, launch support).
4. Avoid scorecard theater; use few outcome metrics.

## Decision guide

- If every team wants embedded SRE but staff is tiny → central platform first.

## Output template

```markdown
# Org design brief
- Goals:
- Structure choice:
- Interfaces / ownership:
- Metrics:
```

## Anti-patterns

- Reorg as substitute for SLOs.
- Scorecards without action.

## Related skills

`sre-engagement-model`, `sre-culture`, `platform-engineering-sre`

## Canonical references

- [SRE Team Lifecycles](https://sre.google/workbook/team-lifecycles/)
- [SRE Book 2e](https://sre.google/books/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
