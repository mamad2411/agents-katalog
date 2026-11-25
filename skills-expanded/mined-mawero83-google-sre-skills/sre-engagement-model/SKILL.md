---
name: sre-engagement-model
description: >-
  Design SRE engagement models: PRR-style gates, tiered engagement, outcomes-focused partnerships, and exit criteria — from Workbook and Book 2e. Use when taking on or offboarding services.
---

# SRE Engagement Model

**Domain:** `organization`  
**Sources:** Workbook Ch18, SRE Book 2e Ch7, SRE Book 1e Ch32

## When to use

- Service wants SRE support
- Defining production readiness
- Ending or pivoting an engagement

## Principles

- Engagements need shared objectives, roles, and success metrics.
- Intent / impact / value should be explicit.
- Models: kitchen-sink, embedded, infra, tools, consulting, blended.
- Engagements should pivot with outcomes — not become infinite tickets.

## Workflow

1. Scope service CUJs and current maturity.
2. Choose engagement type and staffing.
3. Set entry gates (SLO, paging, rollback, owners).
4. Define quarterly outcomes and exit/pivot criteria.
5. Review; renew or end deliberately.

## Decision guide

- If product refuses error budgets → do not fake engagement.

## Output template

```markdown
# Engagement brief
- Service:
- Model:
- Entry gates:
- Outcomes (90d):
- Exit/pivot criteria:
```

## Anti-patterns

- Infinite SRE ownership without product accountability.

## Related skills

`reliable-launches`, `sli-slo-design`, `sre-org-structures`

## Canonical references

- [SRE Engagement Model](https://sre.google/workbook/engagement-model/)
- [Evolving Engagement Model](https://sre.google/sre-book/evolving-sre-engagement-model/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
