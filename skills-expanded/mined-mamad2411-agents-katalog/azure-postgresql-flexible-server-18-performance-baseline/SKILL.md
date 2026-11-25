---
name: azure-postgresql-flexible-server-18-performance-baseline
description: Establishes Azure Database for PostgreSQL Flexible Server 18 sizing and runtime performance baselines. Use when reviewing SKU, storage, IOPS, throughput, connection limits, pooling, query behavior, locks, autovacuum, and production readiness.
license: MIT
compatibility: Requires Azure CLI for resource information. Optional psql is required for PostgreSQL runtime baselines.
---

# Azure PostgreSQL Flexible Server 18 Performance Baseline

## When to Use This Skill

Use this skill for:

- Production readiness sizing review.
- Baseline collection before tuning.
- Connection limit and pooling review.
- Query, lock, and autovacuum symptom review.
- Pre-migration and post-migration performance comparison.

## Core Guidance

- Baseline before tuning.
- Avoid production-impacting diagnostics without explicit approval.
- Treat SKU, storage size, storage type, IOPS, throughput, HA, read replicas, and connection pooling as workload-specific decisions.
- Do not add indexes without query evidence and write-overhead review.
- Run scripts with `--help` before use.

## Workflows

- [performance-baseline-workflow](workflows/performance-baseline-workflow.md)

## Resources

- [performance-baseline-checklist.md](resources/performance-baseline-checklist.md)

## Scripts

- `scripts/collect-performance-baseline.sh`

## Examples

- [performance-baseline.sql](examples/performance-baseline.sql)
