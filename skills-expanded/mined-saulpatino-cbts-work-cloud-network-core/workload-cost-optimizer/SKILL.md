---
name: workload-cost-optimizer
description: Compute-pattern specialist for ML training/inference, serverless (Lambda/Cloud Functions/Azure Functions), and spot/preemptible/low-priority strategies. One agent for the three highest-leverage workload-shape decisions in modern cloud architecture.
---

# Workload Cost Optimizer

> Picks the right compute pattern for the workload -- ML, serverless, or spot -- and tunes it like a different product each time.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/workload-cost-optimizer.md`](../../agents/workload-cost-optimizer.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: workload-cost-optimizer
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Optimize Usage & Cost |
| **Capability** | Workload Optimization |
| **Phase** | Optimize |
| **Primary persona** | Engineering |
| **Collaborating** | FinOps Practitioner, Product |
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

- **Agent:** [`workload-cost-optimizer`](../../agents/workload-cost-optimizer.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
