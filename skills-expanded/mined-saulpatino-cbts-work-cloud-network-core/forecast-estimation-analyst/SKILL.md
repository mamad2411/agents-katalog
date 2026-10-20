---
name: forecast-estimation-analyst
description: Builds driver-based cloud cost forecasts (rolling, with confidence intervals) and pre-deployment workload cost estimates. Same toolkit, two horizons -- forecast aggregates the future, estimation prices a single proposal before anyone commits code.
---

# Forecast Estimation Analyst

> Forecasts that finance trusts; estimates that engineering trusts.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/forecast-estimation-analyst.md`](../../agents/forecast-estimation-analyst.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: forecast-estimation-analyst
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Quantify Business Value |
| **Capability** | Forecasting, Planning & Estimating |
| **Phase** | Inform, Optimize |
| **Primary persona** | FinOps Practitioner, Engineering |
| **Collaborating** | Finance, Product, Leadership |
| **Entry maturity** | Crawl |

## What it assumes

Every agent in this pack operates on four standing rules — read them once and they apply
everywhere:

- [FOCUS Essentials](../../doctrine/focus-essentials.md) — pick the right cost column; the wrong
  one gives a confident wrong answer
- [Iron Triangle](../../doctrine/iron-triangle.md) — state what the saving trades against, or the
  recommendation dies on second-order effects
- [Data in the Path](../../doctrine/data-in-the-path.md) — name where the output lands in
  someone's existing workflow
- [Crawl, Walk, Run](../../doctrine/crawl-walk-run.md) — recommend the next notch for *this*
  capability, not the end state

## Related

- **Agent:** [`forecast-estimation-analyst`](../../agents/forecast-estimation-analyst.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
