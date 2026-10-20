---
name: cloud-onboarding-coordinator
description: Runs the cost-transparent migration process for workloads moving into cloud, between clouds, or between accounts/subscriptions. Designs the intake gate that prevents new workloads from landing untagged, unallocated, and unforecast.
---

# Cloud Onboarding Coordinator

> The migration is done" is never the right time to start doing FinOps.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/cloud-onboarding-coordinator.md`](../../agents/cloud-onboarding-coordinator.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: cloud-onboarding-coordinator
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Manage the FinOps Practice |
| **Capability** | Onboarding Workloads |
| **Phase** | Inform, Operate |
| **Primary persona** | FinOps Practitioner, Engineering |
| **Collaborating** | Finance, Procurement, Leadership |
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

- **Agent:** [`cloud-onboarding-coordinator`](../../agents/cloud-onboarding-coordinator.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
