---
name: wp-performance-audit-planning
description: Plans reproducible WordPress performance audits with explicit scenarios, environments, baselines, budgets, safety boundaries, and evidence requirements.
---

# WordPress performance audit planning

Use this skill before collecting measurements or proposing optimizations.

## Responsibilities

- establish business-critical user journeys;
- inventory runtime and infrastructure context;
- define representative data and cache states;
- choose profiling and benchmarking methods;
- establish budgets and success criteria;
- define safety, privacy, rollback, and evidence boundaries.

## Process

1. Read the four plugin rules.
2. Complete [audit-plan-template.md](resources/audit-plan-template.md).
3. Build a scenario matrix with [scenario-budget-matrix.md](resources/scenario-budget-matrix.md).
4. Use [plan-performance-audit-workflow.md](workflows/plan-performance-audit-workflow.md).
5. Do not begin optimization until a repeatable baseline exists.

## Handoff

The plan must tell the next skill exactly:

- what to measure;
- where to measure it;
- which cache/authentication states matter;
- which tools are approved;
- what evidence may be retained;
- what result would justify remediation.
