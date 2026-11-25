---
name: mssql-operations-debugging
description: "Debug SQL Server plans, Query Store, waits, deadlocks, backups, restore, and HA."
---

# MSSQL Operations Debugging

For bugfix authorization and plan prerequisites, defer to `itsol-workflow-mode`; retain evidence, root-cause analysis, proportionate verification, and final review in every mode.

Use this skill when diagnosing SQL Server production or pre-production issues in .NET systems: slow endpoints, timeouts, high CPU, blocking, deadlocks, log growth, failed migrations, backup/restore risk, failover issues, or connection pool pressure.

## Process

1. State expected behavior, actual symptom, user impact, affected time window, and recent changes.
2. Gather evidence from application logs, traces, metrics, Query Store, execution plans, wait stats, blocking/deadlock data, connection pool behavior, deployment history, and database maintenance state before proposing a fix.
3. Isolate whether the root cause is query shape, missing/wrong index, parameter sniffing, locks, transaction scope, stats, connection pool pressure, migration/backfill, HA/failover, or infrastructure capacity.
4. Implement one root-cause fix or produce a technical fix plan with verification and rollback/roll-forward steps.

## Coordination

Use with `itsol-bug-debugging` for mode-valid Technical Fix Plan state under `itsol-workflow-mode`, `mssql-review` for risk review, `dotnet-web-api-debugging` for API symptoms, and `infra-*` skills when the issue touches deployment, storage, backup, HA, monitoring, or capacity.

## Focused References

- [01-evidence-and-query-diagnostics.md](./references/01-evidence-and-query-diagnostics.md) - Evidence And Query Diagnostics
- [02-blocking-deadlocks-and-playbooks.md](./references/02-blocking-deadlocks-and-playbooks.md) - Blocking Deadlocks And Playbooks
- [03-maintenance-dr-ha-security.md](./references/03-maintenance-dr-ha-security.md) - Maintenance DR HA And Security
