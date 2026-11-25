---
name: kubernetes-finops-engineer
description: Specialist in Kubernetes cost allocation, namespace and label-based chargeback, and cluster-level optimization. Comfortable with OpenCost, Kubecost, Karpenter, cluster autoscaler, and vertical pod autoscaler.
---

# Kubernetes FinOps Engineer

> Allocates every node-hour to a team and every pod-cpu-hour to a workload.

**Depth lives in the agent.** This skill is the trigger surface; the full method, critical
rules, deliverables, and worked maturity tiers are in
[`agents/kubernetes-finops-engineer.md`](../../agents/kubernetes-finops-engineer.md). That file is the single source of truth —
edit it there, not here.

## How to invoke

Delegate to the specialist rather than working from this summary:

```
Agent tool → subagent_type: kubernetes-finops-engineer
```

Give it the concrete question, the dataset or scope it should work from, and the audience for
the output. It assumes the doctrine below without being told.

## FinOps Framework anchors

| | |
|---|---|
| **Domain** | Understand Usage & Cost |
| **Capability** | Allocation |
| **Phase** | Inform |
| **Primary persona** | FinOps Practitioner |
| **Collaborating** | Engineering |
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

- **Agent:** [`kubernetes-finops-engineer`](../../agents/kubernetes-finops-engineer.md)
- **Routing:** [`orchestration/routing.md`](../../orchestration/routing.md) — when to pick this over an adjacent specialist
- **Playbooks:** [`playbooks/`](../../playbooks/README.md) — named failure patterns this agent recognizes
