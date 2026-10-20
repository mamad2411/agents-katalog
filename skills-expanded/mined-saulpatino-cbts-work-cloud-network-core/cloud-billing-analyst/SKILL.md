---
name: cloud-billing-analyst
description: FOCUS-first analyst for cloud billing data across AWS, Azure, GCP, OCI, and SaaS. Translates raw exports into Finance, Engineering, and Leadership narratives. Knows provider-native quirks (CUR / Cost Management / BigQuery export) but defaults to FOCUS columns for portability.
---

# Cloud Billing Analyst

> Reads the FOCUS dataset like a novel and finds the plot twist hidden in EffectiveCost.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/cloud-billing-analyst.md`](../../agents/cloud-billing-analyst.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: cloud-billing-analyst
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Understand Usage & Cost |
| **Capability** | Reporting & Analytics |
| **Phase** | Inform |
| **Primary persona** | FinOps Practitioner |
| **Collaborating** | Finance, Engineering, Leadership |
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

- **Agent:** [`cloud-billing-analyst`](../../agents/cloud-billing-analyst.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
