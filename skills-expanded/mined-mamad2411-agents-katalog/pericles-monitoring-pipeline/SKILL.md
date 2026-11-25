---
name: pericles-monitoring-pipeline
version: 2026.05.0
description: >
  How the monitoring pipeline detects, deduplicates, filters, scores, and persists
  events. Use this WHENEVER you change detection, the content-hash dedup, the Haversine
  geo filter, severity/confidence scoring, the candidate→Validation hand-off, or the
  per-org monitoring process. Encodes the real pipeline in backend/src/monitoring and
  the 13 tools, the SHA-256 event hash, EventHash TTL, and that the Validation Agent
  step is currently a stub.
doctrine_refs: [§3, §4; Ops §1–§2]
depends_on: [pericles-functional-agent, pericles-topical-skill, pericles-data-model, pericles-postgres-queue]
last_reconciled: 2026-05-28
---

# Pericles Monitoring Pipeline (build skill)

The monitoring pipeline is the `pre_validation` spine: it turns raw signal from the
Topical tools into deduplicated, geo-filtered, scored **candidate Events**, then hands
them to Validation. It already exists in `backend/src/monitoring/` and runs as a
standalone per-organization process.

## When to use this skill

Changing detection, dedup, geo filtering, severity/confidence scoring, the
candidate→Validation hand-off, the per-org runner, or monitoring audit/metrics.

## The pipeline (as built)

Per `CLAUDE.md` and the monitoring runtime:

1. **Org context** — `erpContextTool` loads plants, warehouses, suppliers, lanes, and
   `monitored_risk_types` (from `OrganizationContext`).
2. **Run enabled tools** — only data sources enabled per org via `DataSourceToolConfig`;
   the 10 Topical monitors execute (`pericles-topical-skill`).
3. **Deduplicate** — `generateEventHash` =
   `SHA-256(normalizedTitle | normalizedSource | normalizedType | hourBucket)`
   (trim+lowercase; timestamp truncated to the hour to curb hash proliferation). Checked
   against `EventHash` (with `expires_at` TTL) and `Event.event_hash`
   (`pericles-data-model`).
4. **Geographic filter** — Haversine `calculateDistance(lat1,lon1,lat2,lon2)` (km, in
   `weather-disaster-monitor-tool.ts`) keeps events near the org's footprint.
5. **Risk-type filter** — drop events outside the org's `monitored_risk_types`.
6. **Score** — severity (0.0–1.0) and confidence (0.0–1.0).
7. **Persist** — write `Event` rows with `validation_status: pending`.
8. **Hand to Validation** — `validation-client.ts#requestValidation` passes the event on;
   Validation updates `validation_status` and may escalate to `Incident`.

**Important current-state caveat:** `validation-client.ts` is a **placeholder**
(`requestValidation` is a TODO). The Validation Agent is PoC/not wired
(`pericles-functional-agent`, `pericles-evals-scorers`). Today events are persisted with
`validation_status: pending`; the confirmation step is stubbed. Don't assume validated
events flow automatically until that lands.

## Runner & observability

- Standalone process: `npm run monitoring:start -- --organization-id=<uuid>`
  (`monitoring/start.ts` → `startMonitoring`/`stopMonitoring`); config via
  `loadMonitoringConfig` + env overrides; interval `MONITORING_DEFAULT_INTERVAL_MS`
  (default 15000). Requires `DATABASE_URL`. AI keys are org-scoped only
  (`org.<provider>_api_key` in Secrets, no platform fallback) — an org with
  no key has its cycle skipped with a WARN log (`MissingApiKeyError`).
  The monitoring agent's scorer judges ride the same org model+key each
  cycle resolved (`updateScorerJudgeModels`, next to `agent.__updateModel`),
  so no monitoring path reads a platform `OPENAI_API_KEY`.
- Each cycle writes a `MonitoringAuditLog` (event_type `monitoring_cycle`/`source_fetch`/
  `deduplication`/`error`; counts; duration) — `pericles-observability`.
- Durable hand-offs (event/incident/notification) go through `MessageQueue`
  (`pericles-postgres-queue`).

## What this forbids

Changing the hash formula without versioning/migrating `EventHash` (breaks dedup);
skipping `organization_id` scoping or the `monitored_risk_types` filter; persisting
events without a `MonitoringAuditLog` record; assuming Validation runs (it's stubbed);
committing actions from the pipeline (that's an Execution Node — `pericles-execution-node`).

## Verification

Dedup is stable across cycles (same event → same hash → no duplicate); geo + risk-type
filters honor org context; severity/confidence in [0,1]; events persist with
`validation_status` and an audit-log row; the per-org runner respects the interval and
env.

## Existing standards (read alongside)

`CLAUDE.md` (Event Processing Pipeline); `backend/src/monitoring/*`;
`backend/src/mastra/tools/incident-lookup-tool.ts` (`generateEventHash`);
`.cursor/rules/001-application/001-agents/001-monitoring-agent-core-standards-auto.mdc`.

## Open questions

- The Validation Agent contract that replaces the `validation-client.ts` stub — define
  with `pericles-functional-agent` (must reach beyond Monitoring).
- Whether severity/confidence scoring moves into a scorer-gated Skill or stays inline.

## Changelog

- 2026.05.0 — Initial draft from the real monitoring runtime + dedup; flagged the
  Validation Agent stub.
