---
name: azure-cache-redis-7-ops-debugging
description: Debugs Azure Cache for Redis Enterprise and Enterprise Flash Redis 7 incidents and operational issues involving evictions, latency, connections, memory pressure, server load, public access, persistence risk, dangerous commands, and migration readiness.
license: MIT
compatibility: Optional scripts require bash and python3 for hook JSON parsing.
---

# Azure Cache for Redis 7 Ops Debugging

This skill supports safe operational work on Azure Cache for Redis Redis 7.2.

## When to Use This Skill

Use it for:

- Latency and timeout incidents.
- Memory pressure and evictions.
- Connection spikes or authentication errors.
- Server load and throughput symptoms.
- Persistence/data-loss risk review.
- Dangerous Redis or Azure CLI command review.
- Migration readiness to Azure Managed Redis.

## Workflows

- `workflows/incident-triage-workflow.md`: Use during Redis incidents or performance investigations.
- `workflows/persistence-risk-review-workflow.md`: Use when Redis might be acting as durable persistence.
- `workflows/migration-readiness-workflow.md`: Use when preparing to migrate to Azure Managed Redis.

## Resource

- `resources/incident-triage-checklist.md`: Practical incident checklist.

## Script

- `scripts/azure-cache-redis-7-command-guard.sh`: Hook helper that prompts before destructive or secret-exposing commands.

Run scripts with `--help` before manual use.

## Operational Principles

1. Preserve availability before optimizing.
2. Prefer read-only diagnostics first.
3. Confirm cache tier, region, clustering, and geo-replication before taking action.
4. Avoid destructive Redis commands unless explicitly approved.
5. Use bounded sampling and `SCAN`, not `KEYS *`, in production.
6. Capture current metrics before scale, reboot, upgrade, failover, or key rotation.
7. Redact keys and values when they may include sensitive data.
