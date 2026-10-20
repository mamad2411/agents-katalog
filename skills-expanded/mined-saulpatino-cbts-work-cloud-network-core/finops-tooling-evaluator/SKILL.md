---
name: finops-tooling-evaluator
description: Build-vs-buy analysis, vendor selection, and tool-portfolio hygiene for FinOps platforms, k8s cost tools, commitment optimizers, and reporting/BI layers. Picks tools that deliver FinOps Capabilities, not logos.
---

# FinOps Tooling Evaluator

> Starts with native cost tools and graduates to third-party only when the gap is measurable.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/finops-tooling-evaluator.md`](../../agents/finops-tooling-evaluator.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: finops-tooling-evaluator
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Manage the FinOps Practice |
| **Capability** | FinOps Tools & Services |
| **Phase** | Operate |
| **Primary persona** | FinOps Practitioner, Leadership |
| **Collaborating** | Engineering, Procurement, Finance |
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

- **Agent:** [`finops-tooling-evaluator`](../../agents/finops-tooling-evaluator.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
