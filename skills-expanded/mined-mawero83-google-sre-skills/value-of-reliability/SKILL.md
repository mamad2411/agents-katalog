---
name: value-of-reliability
description: >-
  Quantify and communicate the business value of reliability and the cost of unreliability for customers, finance, and engineering velocity. Use when pitching SRE investment, justifying error budgets, or writing exec briefs.
---

# Value Of Reliability

**Domain:** `foundations`  
**Sources:** SRE Book 2e Ch2

## When to use

- Executive asks for ROI of SRE / reliability work
- Prioritizing reliability vs feature work
- Explaining error budgets to product/finance

## Principles

- Unreliability has direct costs, opportunity costs, toil inflation, velocity loss, and retrofit penalties.
- Reliability value accrues to customers, CFO, peer teams, culture, and growth — frame for the stakeholder.
- Early-stage orgs need lighter SRE patterns than mature platform orgs.
- Cost of managing atrophy compounds; postponing reliability work is rarely free.

## Workflow

1. Identify stakeholder (CFO, PM, Eng Dir, customer success).
2. Collect evidence: incidents, lost revenue/time, engineer hours on toil, delayed launches.
3. Translate into 2–3 cost categories with ranges (not fake precision).
4. Propose a reliability investment with measurable outcome (SLO, burn, toil %).
5. Recommend a governance mechanism (error budget policy) so spend is controlled.

## Decision guide

- If numbers are soft → use ranges + leading indicators (pages/week, change failure rate).
- If org is early-stage → argue for lightweight SLOs + on-call hygiene, not a large SRE org.

## Output template

```markdown
# Reliability value brief
- Stakeholder:
- User/business impact of recent unreliability:
- Cost categories (range):
- Proposed investment + success metric:
- Governance (error budget / freeze rules):
```

## Anti-patterns

- Claiming ROI without linking to incidents or customer impact.
- Using uptime marketing numbers as engineering SLOs.

## Related skills

`sre-foundations`, `error-budget-policy`, `sli-slo-design`

## Canonical references

- [SRE books hub (2e overview)](https://sre.google/books/)
- [2e announcement](https://cloud.google.com/blog/products/devops-sre/sre-book-second-edition)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
