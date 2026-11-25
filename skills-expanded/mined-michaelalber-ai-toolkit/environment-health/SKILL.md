---
name: environment-health
audience: team
description: Docker health checks, service monitoring, container lifecycle management, connection validation, and environment diagnostics. Use when troubleshooting dev environment issues or performing health audits.
---

# Environment Health

> "Hope is not a strategy. Monitoring is."
> -- Tom Limoncelli, The Practice of Cloud System Administration

## Core Philosophy

This skill provides the diagnostic toolkit for environment health assessment. It covers Docker container health, service endpoint monitoring, connection validation, port conflict resolution, resource usage analysis, and dependency verification. **Every diagnosis is evidence-based** — no assumptions, no guesses, only verified findings.

**Non-Negotiable Constraints:**
1. **Probe before diagnosing** — discover what is actually running before checking health. Stale assumptions about expected services cause missed diagnoses.
2. **Diagnose before remediating** — understand the root cause before applying a fix. Restarting a container that crashes due to a missing volume just creates a restart loop.
3. **Verify after every action** — confirm the fix actually worked. A service that starts is not necessarily healthy.
4. **Log every command and output** — reproducibility is the foundation of debugging. If you cannot replay the steps, you cannot verify the fix.
5. **Respect environment boundaries** — development environments get autonomous fixes; everything else gets a report.

The domain principles table, AI discipline rules, anti-patterns catalog, and error-recovery
procedures live in `references/diagnostic-discipline.md`.

## Workflow

The full command catalog for each phase is in `references/diagnostic-commands.md` (environment
discovery, Docker health checks, service endpoints, database connections, port conflicts,
resource usage, dependency graph). Docker Compose health-check patterns by service type are in
`references/docker-health-patterns.md`.

```
PROBE       Discover what is running and where before any health check: containers (all
            states), compose services, listening ports, and environment type. No write actions.

DIAGNOSE    Gather evidence per failing service — health status, restart count, log errors,
            endpoint/connection checks, resource pressure, dependency order. Form a root-cause
            hypothesis backed by command output, never assumption.

REMEDIATE   Dev only, after confirming environment=dev. Fix one service at a time; prefer
            restart over recreate, recreate over rebuild. Each action idempotent and logged.

VERIFY      Re-run the same probe that detected the problem. A captured command result, never a
            claim. After a restart, wait, then re-check application-level health before reporting.
```

**Exit criteria:** each finding is backed by command output, remediations are verified by
re-probe, and non-dev environments produce a report rather than mutations.

## State Block

```
<env-health-state>
phase: DIAGNOSE
environment: dev
services_total: 5
services_healthy: 3
services_degraded: 1
services_failing: 1
issues_found: 2
issues_resolved: 0
last_action: Checked container logs for app-worker
last_verified: Database connection healthy on port 5432
blockers: none
</env-health-state>
```

## Output Template

```markdown
## Environment Health Audit: [Project Name]
**Environment**: [dev/staging/prod] | **Date**: [date]

| Service | Status | Health Check | Uptime | Restarts |
|---------|--------|--------------|--------|----------|
| [name]  | [running/stopped] | [healthy/unhealthy/none] | [duration] | [N] |

| Resource | Current | Threshold | Status |
|----------|---------|-----------|--------|
| Disk (/) | [N]% | 80% | [ok/warn/critical] |

| # | Severity | Component | Issue | Status |
|---|----------|-----------|-------|--------|
```

Full templates (Port Mapping table, Dependency Health Map, Remediation Actions log): `references/service-recovery-playbook.md`

## Integration with Other Skills

This is a standalone skill designed for the environment-health-agent. It provides the diagnostic commands, health check patterns, and recovery procedures that the agent executes during its PROBE, DIAGNOSE, REMEDIATE, and MONITOR phases.

Reference files:
- `references/diagnostic-commands.md` — full command catalog per workflow phase
- `references/diagnostic-discipline.md` — domain principles, AI discipline rules, anti-patterns, error recovery
- `references/docker-health-patterns.md` — Docker Compose health checks by service type, container log analysis, network debugging, volume mount verification
- `references/service-recovery-playbook.md` — database connection pool exhaustion, port conflicts, certificate expiry, DNS failures, memory leaks, zombie processes; full output templates
