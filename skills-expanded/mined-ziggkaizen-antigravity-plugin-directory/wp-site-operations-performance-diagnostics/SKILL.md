---
name: wp-site-operations-performance-diagnostics
description: Diagnoses WordPress performance by establishing reproducible baselines, separating frontend, PHP, database, cache, external-service, and infrastructure layers, and testing one hypothesis at a time. Use for slow pages, admin, APIs, cron, or regressions.
---

# wp-site-operations-performance-diagnostics

Use this skill after confirming the issue is performance-related or when performance degradation is one incident dimension.

## Principles

- Measure before changing.
- Compare the same path, user state, cache state, region, and data.
- Separate visitor, authenticated, admin, API, and scheduled workloads.
- Distinguish cache layers and ownership.
- Use staging for invasive profiling or plugin isolation.
- Keep production instrumentation bounded and remove it afterward.
- Verify functionality as well as speed.

## Workflow

Use [`workflows/diagnose-wordpress-performance-workflow.md`](workflows/diagnose-wordpress-performance-workflow.md).

## Resource

Use [`resources/cache-layer-matrix.md`](resources/cache-layer-matrix.md).

## Completion Evidence

Produce baseline and post-change measurements, affected path, cache/user state, evidence by layer, tested hypotheses, selected change, regressions checked, monitoring result, and remaining capacity or risk.
