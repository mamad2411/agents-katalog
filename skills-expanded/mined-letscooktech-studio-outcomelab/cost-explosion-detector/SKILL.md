---
name: cost-explosion-detector
description: Detect and prevent cloud, SaaS, data, and AI cost escalation using billing, usage, architecture, and growth evidence. Use for FinOps reviews, budget variance, pricing changes, AI inference costs, or pre-scale cost design.
---

# Cost Explosion Detector

Apply the shared [OutcomeLab skill standard](../../docs/SKILL-STANDARD.md) for evidence, verification, risk, benchmarking, and improvement.

Trace spend to its technical and commercial drivers, then install guardrails before the next bill does it for you.

## Workflow

1. Reconcile invoice, usage, tags, owners, environments, commits/releases, and business volume for the same time window.
2. Decompose spend into fixed, variable, step-function, and waste categories. Model unit cost per customer, request, workload, or token.
3. Detect high-growth drivers, idle or oversized resources, egress, retry storms, storage retention, pricing-plan drift, and uncapped AI loops.
4. Rank interventions by savings confidence, risk, payback, engineering effort, and reversibility.
5. Define budget alerts, quotas, anomaly thresholds, allocation tags, and a weekly ownership cadence.

## Output contract

Return a spend baseline, driver tree, forecast with assumptions, prioritized savings register, implementation plan, and controls.

## Quality gates

- Separate realized savings from forecasts.
- Do not recommend changes that break SLOs without an explicit trade-off approval.
- Make every cost claim traceable to billing or usage evidence.
