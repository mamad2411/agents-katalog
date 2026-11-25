---
name: boss
description: Executive reporting - delegates to orchestrator/reporting/ for dashboards
type: reference
---

# Boss Skills

This is a **skill reference**. Orchestration logic lives in `orchestrator/reporting/ORCHESTRATOR.md`.

## Atomic Skills

| Skill | Purpose | Single Responsibility |
|-------|---------|----------------------|
| metrics-aggregator | Collect data from ADO, tests, gates | Data collection |
| risk-identifier | Analyze blockers, dependencies, risks | Risk analysis |

## Report Types

Sprint health, release readiness, dependency report, quality trends, performance scorecard, risk dashboard

## Orchestration

For full executive reporting and escalation workflows:
→ See `orchestrator/reporting/ORCHESTRATOR.md`
