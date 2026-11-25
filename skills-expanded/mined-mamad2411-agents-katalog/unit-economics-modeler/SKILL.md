---
name: unit-economics-modeler
description: Builds cost-per-unit models (per request, per tenant, per transaction, per GB) that connect cloud spend to business outputs -- the single most important view for a SaaS FinOps practice.
---

# Unit Economics Modeler

> Makes "cost per customer" a number engineering can move, not a CFO mystery.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/unit-economics-modeler.md`](../../agents/unit-economics-modeler.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: unit-economics-modeler
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Quantify Business Value |
| **Capability** | Unit Economics |
| **Phase** | Inform, Optimize |
| **Primary persona** | FinOps Practitioner |
| **Collaborating** | Product, Finance, Engineering |
| **Entry maturity** | Walk |

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

- **Agent:** [`unit-economics-modeler`](../../agents/unit-economics-modeler.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
