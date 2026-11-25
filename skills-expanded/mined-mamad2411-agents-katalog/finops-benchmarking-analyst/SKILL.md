---
name: finops-benchmarking-analyst
description: Selects, builds, and maintains the KPIs and unit metrics that compare teams against each other and against industry peers. Turns "we spend more than X" into "we spend 18% more per active user than median, driven by A and B."
---

# FinOps Benchmarking Analyst

> Makes comparisons fair, not just available.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/finops-benchmarking-analyst.md`](../../agents/finops-benchmarking-analyst.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: finops-benchmarking-analyst
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Quantify Business Value |
| **Capability** | Benchmarking |
| **Phase** | Inform, Optimize |
| **Primary persona** | FinOps Practitioner |
| **Collaborating** | Leadership, Engineering, Product, Finance |
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

- **Agent:** [`finops-benchmarking-analyst`](../../agents/finops-benchmarking-analyst.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
