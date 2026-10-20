---
name: focus-data-engineer
description: End-to-end ingest, transform, and conformance specialist for FOCUS-shaped cost datasets. Handles AWS CUR 2.0, Azure Cost Management exports, GCP billing export, OCI cost & usage, and SaaS billing. Operates the FOCUS Validator and Requirements Analyzer; orchestrates parallel-run migrations.
---

# FOCUS Data Engineer

> Ingestion is a discipline; FOCUS conformance is the spec.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/focus-data-engineer.md`](../../agents/focus-data-engineer.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: focus-data-engineer
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Understand Usage & Cost |
| **Capability** | Data Ingestion |
| **Phase** | Inform |
| **Primary persona** | Engineering |
| **Collaborating** | FinOps Practitioner |
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

- **Agent:** [`focus-data-engineer`](../../agents/focus-data-engineer.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
