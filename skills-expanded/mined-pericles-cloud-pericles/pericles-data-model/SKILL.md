---
name: pericles-data-model
version: 2026.06.2
description: >
  How to model data in Pericles with Prisma + PostgreSQL. Use this WHENEVER you add
  or change a table, a query, or a migration. Encodes the real schema: organization_id
  on every tenant table, the Event(validation_status) → Incident lifecycle, EventHash
  TTL dedup, the MonitoringAuditLog/AuthAuditLog audit tables, the MessageQueue +
  KeyValueStore infrastructure tables, UserOrganization RBAC, and the Organization
  hierarchy where branded subsidiaries are child orgs — no Kafka, no Redis.
doctrine_refs: [§2, §9; Security §2; Ops §1–§2]
depends_on: [pericles-mastra-tool, pericles-tenant-isolation]
last_reconciled: 2026-06-26
---

# Pericles Data Model (build skill)

Postgres is system of record, queue, and KV store. The model must be safe for strict
multi-tenancy and regulated-industry audit from day one. This skill reflects the
**actual** `backend/prisma/schema.prisma`.

> **Existing rules:** `.claude/rules/05-database.md`,
> `.cursor/rules/500-architecture/506-postgresql-core-standards-auto.mdc`,
> `.cursor/rules/500-architecture/502-prisma-typescript-rules-auto.mdc`.

## Rule 1 — `organization_id` on every tenant table and query

Every tenant row carries `organization_id` (snake_case) with an index (often
composite, e.g. `@@index([organization_id, status])`), an FK to `Organization` with
`onDelete: Cascade`, and every query filters on it. System/global rows use a nullable
`organization_id`. It comes from the authenticated session (`pericles-tenant-isolation`).

## Rule 2 — the real event lifecycle: Event → Incident

The pipeline is **one `Event` table with a `validation_status`**, not separate
candidate/validated tables:

- **`Event`** — raw detected events. `validation_status` ∈ `pending | validated |
  rejected | duplicate`. Carries `event_hash`; unique on `[organization_id,
  event_hash]` and `[organization_id, title, source, type]` (content de-dup).
- **`Incident`** — validated events promoted to incidents (`incident_number` like
  `INC-2025-0001`); `status` ∈ `open | investigating | resolved | closed`.
- **`RiskAssessment`** — agent-generated analysis, linked to an event.
- **`EventHash`** — dedup tracking with `expires_at` (TTL); unique `[organization_id,
  hash]`; index `[organization_id, expires_at]`.

`post_validation` Skills read validated `Event`s / `Incident`s, never the raw signal —
the `validation_status` boundary is "the one defensible version of the truth"
(`pericles-functional-agent`).

## Rule 3 — audit tables exist; keep them append-only

- **`MonitoringAuditLog`** — `event_type` (monitoring_cycle / source_fetch /
  deduplication / error), `source`, `status` (success/failure/partial), counts
  (events_detected/filtered/published, duplicates_found), `duration_ms`,
  error_message/stack, `metadata` Json. The existing monitoring audit record.
- **`AuthAuditLog`** — auth events (event_status SUCCESS/FAILURE).

Treat both as append-only (no app edit/delete path). The full per-invocation Skill
lineage schema (Ops Spec) extends these — see `pericles-observability`. Retention per
manifest `governance.audit_retention_days` (`pericles-compliance-audit`); a
`data-retention-cleanup` job already exists (`npm run jobs:cleanup`).

## Rule 4 — Postgres is the queue and KV store (models already exist)

Do not add Kafka or Redis. The infrastructure tables are present:

- **`MessageQueue`** — `queue_name`, `message_type`, `payload` Json, `status`
  (`MessageStatus`, default PENDING), `attempts`/`max_attempts` (default 3),
  `scheduled_at`/`processed_at`/`failed_at`, `error_message`. Indexes
  `[queue_name, status]`, `[status, scheduled_at]`.
- **`KeyValueStore`** — `key`, `value` Json, `namespace` (default "default", e.g.
  "cache"/"queue"/"session"), `expires_at` (TTL); unique `[organization_id,
  namespace, key]`.

Use these via the existing clients (`pericles-postgres-queue`); do not introduce
parallel job/cache tables.

## Rule 5 — RBAC and org hierarchy (incl. branded subsidiaries)

- **`UserOrganization`** — user↔org with `role` (OWNER/ADMIN/MEMBER/GUEST) and status;
  unique `[user_id, organization_id]`. This is the RBAC substrate.
- **`Organization`** — `is_root` (global-access root); the self-relation
  `parent_organization_id` → `child_organizations` (`"OrganizationHierarchy"`); plus
  per-company brand identity (`name`, `website`, `email_domains`,
  `address_line1`/`city`/`state`/`zip_code`/`country`, `customer_type`).
  **`DataSourceToolConfig`** — per-org enablement of monitoring tools
  (`[organization_id, data_source, tool_id]`, `enabled`).

### Branded subsidiaries are child Organizations, not a column

A customer is frequently a **parent holding company whose operating units are
separately-branded companies**, each with its own supply chain. Public customs (BOL)
data makes this concrete: one parent maps to several distinct importers, each with its
own ImportYeti slug, US address, and supplier base —

- **Helios Technologies** → Sun Hydraulics, Faster, Enovation Controls, Balboa Water
  Group, Daman Products
- **Standex International** → Standex Electronics, Standex Meder, Renco Electronics,
  Bakers Pride, Nor-Lake

Model each subsidiary as **its own `Organization` row**, with `parent_organization_id`
set to the holding company, its own brand fields above, and its own **per-brand**
`OrganizationContext` (suppliers/plants/lanes), `OrganizationSettings`, events,
incidents, and `Supplier`/`Shipment` rows. The parent is a **rollup node**, not the
owner of the children's tenant data: every subsidiary is a full tenant, and every query
stays scoped to a single `organization_id` (`pericles-tenant-isolation`). A parent
"group view" is the **union across child `organization_id`s**, never a relaxation of the
per-row filter.

**Access traverses the hierarchy ancestor → descendant.** `checkOrganizationAccess`
(`backend/src/auth/middleware.ts`) grants access on **direct `UserOrganization`
membership**, **root-org global access**, OR an **active membership in any ancestor
org** (parent rollup — a holding-company member reaches its subsidiaries). Flow is
ancestor → descendant ONLY: a child- or sibling-org member never reaches a parent or
sibling, and the ancestor walk is bounded (cycle-guarded). See `pericles-tenant-isolation`.

**Adapter implication.** An ERP/BOL adapter seeds context **per subsidiary** (one
`OrganizationContext` per child org), because each brand has a distinct footprint.
Flattening several brands' suppliers into one org's context erases the brand boundary
and the per-tenant scope — seed one child org per brand and roll up at the parent
(`pericles-erp-adapter`).

## Rule 6 — cross-customer signal is per-tenant + privacy-preserving (§9)

Signal for cross-customer learning is extracted per tenant with differential-privacy
budgets; aggregation never via direct cross-tenant query (`pericles-org-memory`).

## What this forbids

A tenant table without `organization_id` + index; reading `organization_id` from an
unauthenticated source; mutable audit rows; cross-tenant aggregation without §9 infra;
introducing Kafka/Redis or parallel queue/KV tables alongside MessageQueue/KeyValueStore;
collapsing multiple branded subsidiaries into one `Organization`/`OrganizationContext`
(model each brand as a child org); granting a child- or sibling-org member access to a
parent or sibling (access flows ancestor → descendant only).

## Verification

Migrations reviewed for: `organization_id` + index on every tenant table; correct
`validation_status`/`status` transitions on Event/Incident; EventHash TTL; append-only
audit tables; reuse of MessageQueue/KeyValueStore; no Kafka/Redis. `npm run type-check`
+ `npm run lint` pass (mandatory per CLAUDE.md).

## Existing standards (read alongside)

`CLAUDE.md` (Database Schema, Multi-Tenancy); `.claude/rules/05-database.md`;
`.cursor/rules/500-architecture/{502-prisma-typescript,506-postgresql}-*.mdc`.

## Open questions

- Whether `Incident` fully supersedes `Event` for closed/historical events, or both
  are retained as archive — confirm intended retention with the platform team.

## Changelog

- 2026.06.2 — `checkOrganizationAccess` now traverses the hierarchy ancestor → descendant
  (parent rollup): an active membership in any ancestor org reaches its descendant
  subsidiaries; child/sibling members never reach a parent or sibling. Updated Rule 5 and
  the forbids list accordingly.
- 2026.06.1 — Rule 5 expanded for **branded subsidiaries**: model each separately-branded
  operating unit as a child `Organization` (`parent_organization_id`) with its own
  per-brand `OrganizationContext`; parent is a rollup node (union across child org_ids),
  not the owner of children's data. Adapters seed context per subsidiary. Grounded in
  observed ImportYeti BOL data (Helios, Standex).
- 2026.05.1 — Reconciled against schema.prisma: real models (Event/validation_status,
  Incident, EventHash TTL, MonitoringAuditLog/AuthAuditLog, MessageQueue, KeyValueStore,
  UserOrganization, DataSourceToolConfig, org hierarchy/is_root). Replaced the assumed
  candidate/validated table split.
- 2026.05.0 — Initial draft.
