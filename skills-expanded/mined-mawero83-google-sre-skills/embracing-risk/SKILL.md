---
name: embracing-risk
description: >-
  Apply Google SRE risk thinking: reliability targets below 100%, cost of reliability, and risk as a product decision. Use when setting targets, debating uptime goals, or pushing back on perfectionism.
---

# Embracing Risk

**Domain:** `foundations`  
**Sources:** SRE Book 1e Ch3, SRE Book 2e (risk themes)

## When to use

- Someone wants 100% uptime or five-nines without cost analysis
- Choosing an SLO target
- Balancing launch risk vs reliability

## Principles

- Unplanned downtime budget is a resource — spend it deliberately on innovation.
- The cost of the next nine of reliability rises nonlinearly.
- Manage risk with SLOs + error budgets, not heroics.
- Risk tolerance differs by critical user journey; do not force one number on all paths.

## Workflow

1. List critical user journeys and business impact of failure.
2. Estimate current reliability from data (≥28 days).
3. Propose target with explicit error budget and cost of missing it.
4. Document what happens when budget is spent (policy).
5. Review quarterly; tighten only with evidence of user pain or contract need.

## Decision guide

- If target ≫ current reality → set foundational SLO near reality first.
- If marketing SLA ≠ eng SLO → keep both; never confuse them.

## Output template

```markdown
# Risk / target decision
- Journey:
- Current reliability (window):
- Proposed SLO + budget:
- Cost of next nine (qualitative/quantitative):
- Policy when budget exhausted:
```

## Anti-patterns

- Chasing nines for prestige.
- One global SLO for every microservice.

## Related skills

`sli-slo-design`, `error-budget-policy`, `value-of-reliability`

## Canonical references

- [Embracing Risk](https://sre.google/sre-book/embracing-risk/)
- [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
