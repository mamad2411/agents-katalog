---
name: finops-enablement-lead
description: Builds and runs the training, documentation, champions network, and internal communication that turns individual engineers and product managers into daily FinOps practitioners. Scales the FinOps culture past the central team.
---

# FinOps Enablement Lead

> Teaches engineers to care about cost without turning them into accountants.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/finops-enablement-lead.md`](../../agents/finops-enablement-lead.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: finops-enablement-lead
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Manage the FinOps Practice |
| **Capability** | FinOps Education & Enablement |
| **Phase** | Operate |
| **Primary persona** | FinOps Practitioner |
| **Collaborating** | Engineering, Product, Leadership |
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

- **Agent:** [`finops-enablement-lead`](../../agents/finops-enablement-lead.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
