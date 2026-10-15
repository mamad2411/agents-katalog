---
name: lean-data-platform
description: >
  Blueprint a lean, cost-optimized analytics SaaS on Cloudflare using R2,
  Iceberg, Workers, Pages, Supabase Auth, and Evidence.dev. Use when the user
  wants a multi-tenant reporting platform, white-labeled analytics delivery, or
  a path from a small edge-native deployment to a larger query runtime without
  abandoning Parquet and open table formats.
license: MIT
compatibility: Requires Cloudflare Workers, Pages, R2, and KV access plus an Iceberg-capable ingestion runtime. Optional products include Cloudflare for SaaS and Supabase Auth.
metadata:
  author: Ravishankar Sivasubramaniam
  version: "0.1.0"
argument-hint: <product-or-tenant-context> [constraints]
allowed-tools: Bash
---

## When to use this skill

- Use when the user wants to design or refine a lean analytics platform with **scale-to-zero** compute and **no managed metastore servers**.
- Use when the user wants a **multi-tenant** reporting stack on Cloudflare with R2, Workers, Pages, and custom domains.
- Use when the user wants to combine **open table formats** and **browser-delivered analytics** without defaulting to a heavy warehouse.
- Use when the user wants a **future migration path** to a larger runtime like MotherDuck or BigQuery while keeping Parquet- and Iceberg-oriented storage discipline.

Concrete examples:

- `Design a small multi-tenant analytics SaaS on Cloudflare with Supabase Auth and white-labeled customer report domains.`
- `Show me how to use R2, Iceberg, and Evidence.dev to deliver live reports without a managed BI backend.`
- `Map a path from a lean DuckDB-on-Parquet stack to MotherDuck or BigQuery once concurrency grows.`

## Inputs

- tenant model and isolation requirements
- source data shape such as Excel, CSV, or existing Parquet feeds
- reporting expectations such as embedded dashboards, Evidence.dev pages, or custom domains
- authentication expectations such as Supabase JWT verification, enterprise SSO, or anonymous sharing constraints
- ingestion runtime expectations such as a VM, EC2 instance, Google Cloud VM, or Hetzner host that performs data writes outside the edge runtime
- operational constraints such as low cost, zero egress, no always-on servers, or future warehouse portability

## Progress checklist

- [ ] Resolve the product scope, tenant model, and reporting surface
- [ ] Choose the default small-platform architecture
- [ ] Define storage, catalog, and ingestion flow
- [ ] Define the write plane, report exposure model, and trust boundaries
- [ ] Define tenant isolation and edge authentication
- [ ] Define tenant lifecycle and control-plane behavior
- [ ] Define report delivery and white-label behavior
- [ ] Define observability, maintenance, and degraded-mode behavior
- [ ] Document the future scale-out path and migration triggers
- [ ] Return an implementation-ready blueprint with risks and open questions

## Core policy

1. **Default to the lean edge-native stack**
   - Cloudflare R2 for object storage
   - Apache Iceberg for open table metadata on Parquet
   - R2 Data Catalog as the default Iceberg catalog when the goal is to avoid a dedicated metadata service
   - Workers, Pages, and KV for edge logic, delivery, and lightweight control-plane state
2. **Keep storage open and composable**
   - Parquet is the physical interchange layer
   - Iceberg is the table contract for mutation, schema evolution, and governed datasets
   - avoid proprietary lock-in as the default
3. **Treat browser delivery and governed storage as separate concerns**
   - the system of record can be Iceberg-backed
   - browser-facing Evidence.dev queries should read report-safe Parquet objects or other explicitly exposed read surfaces
   - every answer should name the exposure pattern explicitly such as signed URLs, Worker-mediated APIs, or tenant-scoped materialized report artifacts
4. **Enforce tenant access at the edge**
   - tenant filtering and authorization must happen in Workers or another trusted control layer, not only in the browser UI
   - shared tables with `tenant_id` require a named enforcement path and auditable predicate policy
5. **Prefer scale-to-zero compute until the workload proves otherwise**
   - start with static Pages, Workers, DuckDB-compatible Parquet access, and narrow edge middleware
   - only introduce a larger runtime when concurrency, workload shape, or governance needs justify it
6. **Preserve a warehouse escape hatch**
   - when the browser- and edge-first path becomes limiting, keep the data contract portable to MotherDuck or BigQuery instead of rewriting the whole platform
7. **Keep ingestion external and deliberate**
   - the ingestion and mutation plane may run outside Cloudflare on a VM or instance such as EC2, Google Cloud, or Hetzner
   - do not force the write path into Workers when the user has not asked for that
   - every answer should identify which runtime owns Iceberg writes and where its credentials and schedules live
8. **Design for operations, not only architecture diagrams**
   - include snapshot retention, compaction, schema evolution, logging, and failure handling in the recommendation

## Suggested workflow

1. Resolve the product goal.
   - confirm whether the user needs a hosted analytics portal, an internal reporting app, or a white-labeled customer-facing product
2. Define the small-platform default.
   - R2 + Iceberg + R2 Data Catalog
   - Workers for edge auth and request shaping
   - Pages for Evidence.dev or related frontend delivery
   - KV for hostname-to-tenant and branding lookup
3. Define ingestion discipline.
    - prefer Polars, Arrow, and DuckDB-compatible Parquet outputs
    - make the write plane explicit, typically an external VM or instance that owns Iceberg writes
    - register governed datasets in Iceberg
    - keep report-friendly artifacts predictable and cheap to scan
4. Define the report exposure model.
   - choose one explicit pattern such as signed object access, Worker-mediated data APIs, or tenant-scoped materialized report artifacts
   - name which prefixes, files, or datasets are browser-visible and which are never exposed directly
5. Define multi-tenant enforcement.
    - use Iceberg namespaces or prefix conventions for tenant isolation
    - use JWT-derived tenant context for edge enforcement
    - call out when shared-table designs need strict tenant predicates and auditable access policy
6. Define tenant lifecycle and control plane.
   - how tenants are provisioned
   - how hostnames, branding, and access rules are registered
   - how offboarding, suspension, and data deletion are handled
7. Define reporting and white-label delivery.
    - Evidence.dev in SPA mode for browser-delivered report UX
    - range-friendly Parquet access for DuckDB-Wasm scans
    - Cloudflare for SaaS for custom domains
    - Worker-based branding injection keyed by hostname
8. Define observability and maintenance.
   - auth failures, tenant mismatch, and report access should be logged with tenant context
   - ingestion should emit job status and table-maintenance signals
   - define retention, compaction, and schema-change handling for Iceberg tables
9. Define the future runtime path.
    - stay on the lean stack for moderate scan-heavy reporting
    - graduate selected workloads to MotherDuck or BigQuery when joins, concurrency, freshness, or governance exceed browser- and edge-friendly limits
10. Return the architecture with clear boundaries.
    - what is the default
    - what changes later
    - what remains open or risky

## Gotchas

- Do not assume an in-browser SQL engine is also the authoritative governance layer for multi-tenant access.
- Do not assume browser-delivered reporting can safely consume arbitrary Iceberg tables directly; define the exposed read surface explicitly.
- Do not put tenant isolation only in frontend code; enforce it in a trusted Worker or equivalent backend edge layer.
- Do not leave the ingestion runtime implied; state which external runtime owns writes, scheduling, and secrets.
- Do not add always-on servers for a problem that R2, Workers, Pages, and a managed catalog already solve.
- Do not jump to BigQuery or MotherDuck prematurely; treat them as scale-out options, not the day-one default.
- Do not describe Iceberg as "done" once files are registered; retention, compaction, and schema evolution rules still matter.
- Do not treat white-labeling as only a theming concern; provisioning, suspension, and domain ownership workflows matter too.
- Do not quote Cloudflare pricing, limits, or feature availability without checking current docs first.

## Available scripts

- No bundled executable scripts yet. Use `references/` for architecture guidance and `snippets/` for reusable implementation patterns.

## Output contract

Each run should produce or describe:

1. **Platform summary**
   - the target product shape
   - the recommended default architecture
   - the core reasons for that choice
2. **Component map**
   - storage and table layer
   - write plane and control-plane stores
   - auth and tenant enforcement
   - reporting delivery
   - branding and custom-domain control plane
3. **Trust boundary map**
   - what is browser-visible
   - what only Workers can access
   - what only the external ingestion runtime can mutate
4. **Data flow**
    - ingestion path from Excel or CSV to Parquet and Iceberg
    - query path for reports
    - where tenant context is enforced
5. **Read/write ownership**
   - which runtime owns writes
   - which runtime serves report reads
   - where secrets and credentials live
6. **Tenant lifecycle**
   - provisioning
   - custom-domain and branding registration
   - suspension, offboarding, and deletion path
7. **Operations and maintenance**
   - logging and audit events
   - snapshot retention and compaction
   - schema-change and report-breakage handling
8. **Scale boundaries**
    - what the small-platform design handles well
    - what workload signals justify MotherDuck or BigQuery
9. **Risks and open questions**
    - unresolved auth, domain, governance, or report-exposure choices
10. **Failure and fallback behavior**
   - what happens when auth, catalog, domain, or ingestion dependencies fail
   - what degraded modes are acceptable
11. **Implementation next steps**
    - concrete build order
    - required bindings, secrets, or external services

## Progressive disclosure

Load supporting material selectively:

- Read `references/architecture-blueprint.md` for the default stack and component roles.
- Read `references/tenant-isolation.md` when the user asks about namespaces, JWT enforcement, or shared-table tenancy.
- Read `references/report-exposure-model.md` when the user asks how reports safely read data from R2 or whether the browser can access Parquet directly.
- Read `references/ingestion-and-write-plane.md` when the user asks where ingestion runs, who owns Iceberg writes, or how spreadsheets become curated datasets.
- Read `references/reporting-and-whitelabel.md` when the user asks about Evidence.dev, browser queries, custom domains, or edge branding.
- Read `references/tenant-lifecycle.md` when the user asks how tenants are provisioned, suspended, or deleted.
- Read `references/operations-and-observability.md` when the user asks about logging, maintenance, retention, auditability, or failure handling.
- Read `references/runtime-evolution.md` when the user asks whether to stay lean or move to MotherDuck or BigQuery.
- Read `references/gotchas.md` when the design risks confusion between governed storage, report-serving surfaces, and tenant enforcement.
- Use `assets/blueprint-template.md` when the user wants a written architecture handoff.
- Use `snippets/zero-copy-ingestion.md` when outlining the ingestion path from row-oriented files to Iceberg.
- Use `snippets/worker-tenant-routing.md` when sketching Worker middleware for hostname routing, JWT validation, and brand lookup.

## Failure modes

- If required Cloudflare products are unavailable on the target account, state the exact missing dependency and propose the nearest viable fallback.
- If the report-exposure model is not explicitly defined, do not claim the design is safe for browser-delivered analytics.
- If the ingestion runtime is unspecified, state that an external VM or instance must own writes and maintenance until a different write plane is chosen.
- If the tenant-isolation model is ambiguous, stop short of claiming the architecture is secure and list the unresolved decisions.
- If tenant provisioning, suspension, or offboarding are not defined, call out the operational gap explicitly.
- If retention, compaction, or schema-evolution rules are missing, call out the lakehouse maintenance gap explicitly.
- If observability is absent, say that the design is not yet production-ready even if the component diagram looks correct.
- If the user asks for strict row-level enforcement without a trusted execution layer, call out that browser-only enforcement is insufficient.
- If the requested workload obviously exceeds a lean edge-native design, say so explicitly and recommend the next runtime tier instead of pretending the default stack will hold.
