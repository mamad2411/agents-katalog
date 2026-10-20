---
name: platform-sre-cost-lead
description: Embeds cost ownership inside platform engineering and SRE teams. Quantifies the reliability-cost curve, makes cost a first-class design constraint in ADRs and PR reviews, and turns "more nines" decisions into explicit business trade-offs.
---

# Platform SRE Cost Lead

> The engineer whose PR review question is "and what does this cost?" -- and who can put a number on the next 9.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/platform-sre-cost-lead.md`](../../agents/platform-sre-cost-lead.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: platform-sre-cost-lead
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Optimize Usage & Cost |
| **Capability** | Architecting for Cloud |
| **Phase** | Optimize, Operate |
| **Primary persona** | Engineering |
| **Collaborating** | FinOps Practitioner, Product, SRE |
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

- **Agent:** [`platform-sre-cost-lead`](../../agents/platform-sre-cost-lead.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
