---
name: cloud-sustainability-analyst
description: Measures cloud carbon footprint, identifies lowest-carbon region / service / architecture choices, and quantifies the cost-vs-carbon trade-off for Engineering and Product decisions.
---

# Cloud Sustainability Analyst

> Makes carbon a first-class efficiency metric alongside dollars and latency.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/cloud-sustainability-analyst.md`](../../agents/cloud-sustainability-analyst.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: cloud-sustainability-analyst
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Optimize Usage & Cost |
| **Capability** | Cloud Sustainability |
| **Phase** | Inform, Optimize |
| **Primary persona** | FinOps Practitioner, Engineering |
| **Collaborating** | Sustainability, Leadership, Product |
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

- **Agent:** [`cloud-sustainability-analyst`](../../agents/cloud-sustainability-analyst.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
