---
name: repo-observability-design
description: Designs repository-level observability for services, features, jobs, APIs, data pipelines, and operational workflows. Use when adding or reviewing logs, metrics, traces, dashboards, health checks, instrumentation, ownership, or production readiness signals.
---

# Repository Observability Design

Use this skill when a change needs operational visibility.

## When to Use This Skill

Use this skill for:

- new services, APIs, jobs, workers, data pipelines, or integrations
- reliability-sensitive features
- production readiness reviews
- observability gap analysis
- service ownership and dashboard design
- health checks and readiness checks
- adding logs, metrics, traces, or operational events

## Design Process

1. Identify the operational questions the change must answer.
2. Identify the users, dependencies, queues, stores, and external systems involved.
3. Choose signals using `resources/signal-selection-matrix.md`.
4. Ensure every signal has stable names, useful dimensions, and clear ownership.
5. Avoid high-cardinality or sensitive labels.
6. Define dashboards or views for symptom, cause, and recovery.
7. Define validation and rollback visibility.
8. Document operational assumptions and gaps.

## Workflow

Use `workflows/observability-design-workflow.md` for feature, service, or production-readiness observability design.

## Scripts

This skill owns:

```text
scripts/observability-config-scan.py
```

Run the script with `--help` before manual use.
