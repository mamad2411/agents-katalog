---
name: model-drift-monitoring
description: "Detect model degradation in production: data and prediction drift metrics, delayed-label evaluation, alert thresholds and a triage path that ends in a decision."
type: procedural
category: ai
domain: ai
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - model drift detection
  - data drift monitoring
  - concept drift alert
  - psi ks test features
  - model performance degradation
aliases:
  - drift-monitoring
keywords:
  - drift
  - monitoring
  - psi
  - ks-test
  - concept-drift
  - alerts
  - performance
mcp_servers:
  - grafana
  - prometheus
  - postgres
source: custom
enabled: true
---

# Model Drift Monitoring

## Purpose

Detect model degradation in production: data and prediction drift metrics, delayed-label evaluation, alert thresholds and a triage path that ends in a decision.

## When to Use

- A deployed model's inputs or outcomes change over time.
- Labels arrive late, so accuracy cannot be computed in real time.
- Monitoring exists but no alert has ever led to an action.

## When NOT to Use

- The model runs on a fixed offline dataset.
- The system is deterministic with no learned component.
- There is no ground truth and never will be.

## Capabilities

- Track input feature distributions with PSI or KS per feature.
- Monitor prediction distributions and business outcomes.
- Evaluate against delayed labels with a lag-aware pipeline.
- Set thresholds from historical variability, not gut feeling.
- Define the triage decision: retrain, roll back, or accept.

## Inputs

- The feature list with expected ranges and importance.
- Label arrival lag and the join key.
- The business metric the model influences.

## Workflow

1. Baseline feature and prediction distributions from the training period.
2. Compute PSI/KS daily per important feature; alert on the ones that matter.
3. Join delayed labels when they arrive and compute real performance.
4. Set thresholds from historical noise so alerts mean something.
5. Write a triage runbook: who investigates, and what action follows each trigger.
6. Review alert precision monthly and tune or delete noisy monitors.

## Tools

- evidently
- prometheus
- grafana
- mlflow

## Examples

- `PSI above 0.2 on a top feature predicts degradation weeks before labels arrive.`
- `An alert nobody acts on costs attention; track alert-to-action rate.`

## Safety

- Drift monitoring must not capture per-user data without a privacy basis.
- Never auto-retrain from unvalidated production labels.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `grafana` | stdio | full | medium | `GRAFANA_URL`, `GRAFANA_API_KEY` |
| `prometheus` | stdio | full | medium | `PROMETHEUS_URL` |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/ai/model-drift-monitoring`). First-party skill, maintained in this repository.

## Notes

- Input drift without performance drop is not an incident, it is information.
- Prediction drift catches problems when labels are delayed or missing.
- Pairs with: `mlops`, `agent-observability`.
