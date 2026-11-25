---
name: pericles-observability
version: 2026.05.1
description: >
  How Skill invocations are logged, traced, and operated in Pericles. Use this
  WHENEVER you add an invocation path, emit logs, build a dashboard, or need lineage
  for "why did the platform do X". Reflects the existing instrumentation
  (MonitoringAuditLog, Mastra observability/AI tracing, PinoLogger, monitoring/metrics
  + error-reporter, socket.io realtime) and the target per-invocation lineage schema
  that extends it.
doctrine_refs: [Ops §1–§7; §4, §11]
depends_on: [pericles-data-model]
last_reconciled: 2026-05-28
---

# Pericles Observability (build skill)

The doctrine promises auditability, lineage, and registry-enforced contracts — none
real without instrumentation. "Why did the Plan Executor send that notification" must
be answerable deterministically.

## When to use this skill

Adding/modifying any invocation path; emitting logs; building/changing a dashboard;
implementing audit or lineage features; cost attribution.

## What exists today

- **Mastra observability is ON** (`backend/src/mastra/index.ts`:
  `observability: { default: { enabled: true } }` → DefaultExporter + CloudExporter
  for AI tracing). Telemetry is disabled (deprecated). Logger is **PinoLogger**.
- **`MonitoringAuditLog`** (Prisma) records each monitoring cycle: `event_type`
  (monitoring_cycle / source_fetch / deduplication / error), `source`, `status`
  (success/failure/partial), counts (detected/filtered/published, duplicates),
  `duration_ms`, error_message/stack, `metadata`. **`AuthAuditLog`** records auth.
- **`backend/src/monitoring/`** has `metrics.ts`, `error-reporter.ts`, `logger.ts`,
  and per-tool loggers (`tools/tool-logger.ts`).
- **`socket.io`** provides realtime push to the frontend (the role the PRDs assign to
  Kafka streaming — done over websockets, not Kafka).

## Target: the per-invocation lineage schema (extends the above)

The Ops Spec requires every Skill invocation to log a structured event. Build this as
an extension of `MonitoringAuditLog` (or a sibling `SkillInvocationLog`) with ALL of:

`invocation_id`; `parent_invocation_id`; `skill_id` (with version); `tenant_id`
(always); `user_id`; `triggered_by` (user_query|schedule|pipeline_event|manual_admin|
gateway_path); `inputs_hash` (never raw inputs); `started_at`/`completed_at`/
`duration_ms`; `outcome` (success|error|timeout|rejected_by_governance);
`dependencies_resolved`; `knowledge_sources_queried`; `gateway_path_used`;
`eval_scores`; `error_class`; `tokens_used`.

The `parent_invocation_id` chain reconstructs full lineage — the mechanism behind §4's
defensible answer and §3's per-commit logging (proposing Skill version + inputs + rule
path). Until that table exists, `MonitoringAuditLog.metadata` carries partial lineage.

## Retention

Hot: Postgres, 90 days, tenant-scoped per row. Cold: S3-compatible beyond 90d per
manifest `governance.audit_retention_days` (default 365). Customer deletion: hot
purged within 30d (a `data-retention-cleanup` job exists — `npm run jobs:cleanup`).
Root org reads aggregated/anonymized cross-tenant only — never raw.

## Five dashboards to build/operate against

Skill health (rate, p50/p95/p99, error/timeout, avg scorer score); Eval drift (>2σ
alert — `pericles-evals-scorers`); Dependency graph (orphans, high-fanout, cycles);
Cost attribution (tokens + external-API calls per Skill/tenant); Gateway-path activity
(fresh-signal fetches by cross-pipeline Skills). The monitoring `metrics.ts` is the
seed for Skill-health.

## Customer audit access

Standard/Enterprise: 90-day filterable view, lineage tree, CSV/JSON/PDF export,
Enterprise API. Express: 30-day filter-only. Read-only; never editable/deletable by
customer action (deletion follows the §9 process).

## SLA targets

99.9% invocation availability/qtr; Functional p95 <5s; Topical p95 <3s; eval pipeline
<1h; composition validation <100ms/Skill; audit query (90d) <2s.

## What this forbids

Invocations without the full lineage fields (once the log exists), esp. `tenant_id`,
`parent_invocation_id`, `gateway_path_used`; logging raw inputs (use `inputs_hash`);
any customer path that edits/deletes audit logs; cross-tenant log reads except
aggregated by root.

## Verification

New invocation paths emit the required fields; lineage reconstructs end to end in a
test (parent → children); retention + tenant-scoping enforced per row; dashboards
reflect new Skills within the eval-pipeline SLA.

## Existing standards (read alongside)

`CLAUDE.md` (Mastra config); `backend/src/monitoring/{metrics,error-reporter,logger}.ts`;
`.cursor/rules/500-architecture/513-telemetry-metrics-core-standards-auto.mdc`.

## Open questions

- Whether to extend `MonitoringAuditLog` vs add a dedicated `SkillInvocationLog` for
  the per-invocation lineage schema — decide with the platform team.
- Multi-region log aggregation without violating residency (Ops Spec §8).

## Changelog

- 2026.05.1 — Reconciled: documented existing MonitoringAuditLog/AuthAuditLog, Mastra
  observability/AI tracing, PinoLogger, monitoring metrics/error-reporter, socket.io;
  framed the per-invocation schema as an extension of what exists.
- 2026.05.0 — Initial draft.
