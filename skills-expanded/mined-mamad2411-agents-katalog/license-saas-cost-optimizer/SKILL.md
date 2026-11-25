---
name: license-saas-cost-optimizer
description: Specialist in software licenses and SaaS entitlements in the cloud era. BYOL vs cloud-native licensing, marketplace vs direct, entitlement audits, and the compliance minefield of Microsoft / Oracle / Red Hat / SAP in the cloud.
---

# License Saas Cost Optimizer

> Reads every EULA so Engineering doesn't have to, and always checks the true-up clause.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/license-saas-cost-optimizer.md`](../../agents/license-saas-cost-optimizer.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: license-saas-cost-optimizer
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Optimize Usage & Cost |
| **Capability** | Licensing & SaaS |
| **Phase** | Inform, Optimize, Operate |
| **Primary persona** | FinOps Practitioner, Procurement |
| **Collaborating** | ITAM, Engineering, Finance |
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

- **Agent:** [`license-saas-cost-optimizer`](../../agents/license-saas-cost-optimizer.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
