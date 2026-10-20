---
name: db-failover-checklist
description: >
  Execute and rehearse database failover checklists for owned primary/replica
  systems (Postgres, MySQL, cloud managed): promotion, DNS/endpoint cutover,
  app reconnect, lag verification, and failback. Use during DR drills or real
  incidents — not for unauthorized disruption of third-party data stores.
---

# DB Failover Checklist

## Scope And Authorization

- **In scope:** Databases you operate (self-managed or cloud) with documented DR roles.
- **Out of scope:** Triggering failovers on systems outside your ownership; chaos without approval.
- Prefer scheduled game days; production failover needs incident commander.
- Redact connection strings and credentials in notes.
- Pair with `database-migration-safety` (avoid DDL during failover) and observability skills.

## When To Use

- Primary DB unhealthy beyond SLO.
- Planned maintenance requiring role swap.
- DR/game-day rehearsals.
- Validating RPA/RTO after topology changes.
- Cloud Multi-AZ / replica promotion drills.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Schema migrations | `database-migration-safety` |
| Expand/contract | `db-migration-expand-contract` |
| App retry storms | `retry-backoff-patterns` |
| Full multi-region product design | architecture DR skills |
| Implementation quality baseline | `code-quality-standards` |

## Roles and terms

| Term | Meaning |
| --- | --- |
| Primary/writer | Accepts writes |
| Replica/reader | Async/sync standby |
| Promotion | Replica becomes writer |
| RPO | Data loss tolerance |
| RTO | Time to restore service |
| Split-brain | Two writers — avoid |

## Pre-failover readiness (checklist)

- [ ] Topology diagram current (primary, replicas, proxies, DNS)
- [ ] Credentials/secrets for promotion automation available to on-call
- [ ] Monitoring: lag, connections, disk, failover alerts
- [ ] App uses multi-host URLs / proxy (PgBouncer, ProxySQL, RDS endpoint) not single sticky IP without plan
- [ ] Backups recent + restore tested
- [ ] Runbook owner identified
- [ ] Communication channel (status page) ready

## Workflow

### 1. Detect and decide

1. Confirm primary failure (not just one client network path).
2. Check replica lag — if lag >> RPO, escalate data-loss decision.
3. IC decides: failover now vs wait for primary recovery.

### 2. Freeze risky work

1. Pause deploys and migrations.
2. Block non-essential analytics heavy queries if they impede recovery.
3. Snapshot metrics/logs for postmortem.

### 3. Promote (engine-specific)

#### Cloud managed (pattern)

```bash
# Examples — use your provider's current CLI
# aws rds failover-db-cluster --db-cluster-identifier ...
# az postgres flexible-server ...
```

#### Postgres self-managed (conceptual)

```bash
# On chosen replica — follow your Patroni/repmgr/Stolon process, e.g.:
# patronictl switchover / failover
# Verify: SELECT pg_is_in_recovery();  -- should be false on new primary
```

#### MySQL (conceptual)

```bash
# Orchestrator / MHA / Group Replication procedures per your stack
# STOP SLAVE; reset; promote; re-point others
```

**Never** allow old primary to accept writes until re-introduced as replica.

### 4. Cut application traffic

1. Update writer endpoint (DNS TTL considerations, proxy config, k8s secret, service discovery).
2. Bounce pools if required (PgBouncer `RELOAD`, app connection recycle).
3. Verify writers succeed; readers follow policy (may be degraded).

```bash
# App health
curl -sS https://app.example.local/healthz
# DB
psql "$WRITER_URL" -c 'select now(), pg_is_in_recovery();'
```

### 5. Validate data and lag

1. Critical transaction smoke tests (create/read).
2. Check sequence/identity behavior if applicable.
3. Rebuild or re-attach former primary as replica only via controlled procedure (rewind/rebuild).
4. Watch error budgets and lag for 30–60+ minutes.

### 6. Communicate

1. Incident timeline; customer impact; RPO estimate if any.
2. Next steps for failback window.

### 7. Failback (planned)

1. Only when old node healthy and resynced.
2. Prefer controlled switchover off-peak.
3. Same validation checklist as failover.
4. Postmortem + runbook updates.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Decision | Lag vs RPO explicit | Promote blindly |
| Old primary | Fenced / isolated | Both nodes writable |
| Apps | Connection retry + new endpoint | Permanent connection cache to dead IP |
| Drills | Game day quarterly | First failover is production Sev-1 |
| Migrations | Paused | Run expand DDL mid-failover |

## Output Checklist

- [ ] Failure confirmed and IC assigned
- [ ] Lag/RPO assessed
- [ ] Deploys/migrations frozen
- [ ] Promotion completed via approved tool
- [ ] Writer endpoint cutover done
- [ ] Smoke tests passed
- [ ] Old primary fenced
- [ ] Stakeholders informed
- [ ] Failback plan scheduled
- [ ] Postmortem actions filed

## Rules

- Prevent split-brain above all.
- Rehearse before disaster.
- Focus on **DB failover execution checklist**.
