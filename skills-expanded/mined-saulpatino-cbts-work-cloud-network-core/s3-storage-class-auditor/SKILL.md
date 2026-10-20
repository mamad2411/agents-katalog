---
name: s3-storage-class-auditor
description: Audits S3 (and equivalent object storage) for objects in the wrong storage class. Moves cold data to Glacier, lifecycle-policies new data, and stops the default Standard drift.
---

# S3 Storage Class Auditor

> Cold data in Standard storage is money lit on fire.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/s3-storage-class-auditor.md`](../../agents/s3-storage-class-auditor.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: s3-storage-class-auditor
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
| **Collaborating** | FinOps Practitioner |
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

- **Agent:** [`s3-storage-class-auditor`](../../agents/s3-storage-class-auditor.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
