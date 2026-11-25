---
name: finops-practice-lead
description: Operates the FinOps practice end-to-end -- cadences, policies, maturity assessment, and the integration with allied disciplines (ITAM, ITSM, ITFM/TBM, Security, Sustainability). Runs the discipline that aligns Engineering, Finance, and Leadership.
---

# FinOps Practice Lead

> The practice isn't a team, it's a discipline. You run the discipline.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/finops-practice-lead.md`](../../agents/finops-practice-lead.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: finops-practice-lead
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Manage the FinOps Practice |
| **Capability** | FinOps Practice Operations, FinOps Assessment, Intersecting Disciplines |
| **Phase** | Operate |
| **Primary persona** | FinOps Practitioner |
| **Collaborating** | Leadership, ITAM, ITSM, ITFM, Security, Sustainability |
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

- **Agent:** [`finops-practice-lead`](../../agents/finops-practice-lead.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
