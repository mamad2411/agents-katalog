---
name: disaster-recovery
description: "Plan and prove recovery: RTO/RPO, backup strategy and restore drills, failover runbooks, dependency maps and game days that find the real gaps."
type: procedural
category: devops
domain: devops
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: high
level: advanced
triggers:
  - disaster recovery plan
  - rto rpo definition
  - backup restore drill
  - failover runbook
  - game day exercise
aliases:
  - dr
  - bcp
keywords:
  - disaster-recovery
  - rto
  - rpo
  - backup
  - restore
  - failover
  - runbook
mcp_servers:
  - kubernetes
  - postgres
  - grafana
source: custom
enabled: true
---

# Disaster Recovery

## Purpose

Plan and prove recovery: RTO/RPO, backup strategy and restore drills, failover runbooks, dependency maps and game days that find the real gaps.

## When to Use

- A service has data or availability obligations it cannot currently prove.
- Backups exist but have never been restored.
- A region or dependency failure would be discovered during the incident.

## When NOT to Use

- There is no production system yet.
- The requirement is a single-node dev environment.
- A vendor's SLA is being treated as a substitute for your own plan.

## Capabilities

- Define RTO and RPO per service with the business, not for it.
- Design backups for restore speed, with verified integrity.
- Document failover and failback with the exact commands.
- Map dependencies and their single points of failure.
- Run game days that produce fixes, not just reports.

## Inputs

- Service tiers and their tolerance for downtime and data loss.
- Current backup jobs, retention and storage location.
- The dependency graph, including DNS, identity and third parties.

## Workflow

1. Agree RTO/RPO per tier and write them down where the business can see them.
2. Choose backup type, frequency and retention to meet the RPO, and encrypt at rest.
3. Restore into a clean environment on a schedule; time it and record the real RTO.
4. Write runbooks with exact commands, owners and decision points.
5. Run a game day that kills a dependency and measures the response.
6. Fix what the drill exposed and re-run; the plan is only real after a restore.

## Tools

- velero
- pg_basebackup
- terraform
- chaos-mesh
- pgbouncer

## Examples

- `An untested backup has an unknown RTO; the first restore in an incident is the drill.`
- `RPO 15 minutes requires WAL archiving, not a nightly dump.`

## Safety

- Restores must never overwrite production; always target an isolated environment first.
- Backup credentials are as sensitive as production credentials — separate them.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `kubernetes` | stdio | full | high | `KUBECONFIG` |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |
| `grafana` | stdio | full | medium | `GRAFANA_URL`, `GRAFANA_API_KEY` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/devops/disaster-recovery`). First-party skill, maintained in this repository.

## Notes

- Failback is usually harder than failover and is the part that gets skipped.
- Record restore timings; the trend is the early warning.
- Pairs with: `platform-engineering`, `agent-reliability`.
