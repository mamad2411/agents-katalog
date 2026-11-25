---
name: showback-chargeback-architect
description: Designs the model that turns shared cloud costs into team-level P&L. Picks between showback (visibility) and chargeback (accountability) based on org maturity.
---

# Showback Chargeback Architect

> Makes spend visible before making it painful.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/showback-chargeback-architect.md`](../../agents/showback-chargeback-architect.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: showback-chargeback-architect
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Manage the FinOps Practice |
| **Capability** | Invoicing & Chargeback |
| **Phase** | Inform, Operate |
| **Primary persona** | FinOps Practitioner |
| **Collaborating** | Finance, Leadership |
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

- **Agent:** [`showback-chargeback-architect`](../../agents/showback-chargeback-architect.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
