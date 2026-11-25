---
name: design-multi-tenancy
description: Architects a SaaS so many customer orgs share infrastructure without leaking into each other — picking an isolation model (shared schema + Postgres RLS, schema-per-tenant, or database-per-tenant) against an explicit cost/blast-radius/ops tradeoff table, resolving and propagating tenant context from request to DB session, and enforcing isolation in depth (app-layer query scoping PLUS RLS as the safety net) so a single forgotten tenant filter can't cross-leak. Also covers per-tenant quotas/noisy-neighbor mitigation, fan-out migrations across thousands of tenants, tenant offboarding (export + hard delete), optional per-tenant keys, and safe cross-tenant admin features.
when_to_use: Building or hardening a multi-tenant SaaS where many customer organizations share infra and must be isolated from one another — choosing an isolation model, stopping cross-tenant data leaks, scoping every query by tenant, or scaling migrations/quotas across many tenants. Distinct from design-relational-schema (general table/normalization modeling — this is the tenancy/isolation layer built on top of that), design-authorization-model (what a user may do WITHIN one tenant — RBAC/ABAC — vs separating tenants from each other), and map-privacy-data-gdpr (PII rights/consent — referenced for export/delete mechanics but not the focus).
---

## When to Use

Reach for this skill when the question is **"how do I keep tenant A's data away from tenant B while they share the same stack?"** — the isolation architecture, not the per-user permissions inside one org:

- "We're going multi-tenant — shared tables with a `tenant_id`, a schema per customer, or a DB per customer?"
- "How do I make sure one missing `WHERE tenant_id` can't leak another org's data?"
- "Resolve the tenant from the subdomain / `X-Tenant` header / JWT org claim and scope every query to it"
- "We have 4,000 tenants — how do I run a schema migration across all of them safely?"
- "Enterprise customer wants their data in a separate database / their own encryption key"
- "One big tenant is hammering the DB and starving everyone else (noisy neighbor)"
- "Build admin impersonation / global analytics without accidentally bypassing isolation"

NOT this skill:
- Designing the tables/keys/normalization themselves (PKs, 1:N, constraints) → **design-relational-schema** (this skill adds the `tenant_id` + RLS layer on top of that model)
- Roles/permissions for users *within* a single tenant (admin vs viewer, per-resource sharing) → **design-authorization-model** (authZ within a tenant ≠ isolating tenants from each other)
- DSAR export format, consent capture, lawful basis, erasure-across-backups policy → **map-privacy-data-gdpr** (referenced in step 7 for the offboarding mechanics)
- Capping request *rate/volume* per caller mechanics (token bucket, 429, Redis counters) → **rate-limiting** (referenced in step 6 for per-tenant quotas)
- Running one risky `ALTER` on one large live table safely (locks, backfill) → **db-migration-safety** (referenced in step 8 for the fan-out)
- Cache patterns/TTLs/stampede in general → **caching-strategy** (referenced in step 9 for tenant-keyed caches)

## Steps

1. **Pick the isolation model from a tradeoff table — default shared+RLS, escalate per tenant only when a reason demands it.** The three models are not all-or-nothing; a mature SaaS often runs *hybrid pods*.

   | Dimension | Shared schema + RLS | Schema-per-tenant | Database-per-tenant |
   |---|---|---|---|
   | **Isolation** | Logical (one bug from leak) | Stronger (namespace) | Strongest (physical) |
   | **Cost / tenant** | Lowest (one DB, shared) | Low–medium | Highest (conn pool, idle DB, backups each) |
   | **Ops / migration burden** | One migration, all tenants | Loop over N schemas | Loop over N databases (heaviest) |
   | **Blast radius** | All tenants (shared) | Per-schema | Per-tenant only |
   | **Noisy neighbor** | Worst — shared buffers/CPU/locks | Some sharing | Isolated resources |
   | **Per-tenant restore / PITR** | Hard (row-level surgery) | Medium | Trivial (restore that DB) |
   | **Tenant count it scales to** | 100k+ | hundreds–low thousands | tens–low hundreds |

   Pick: **shared schema + RLS by default** (cheapest, scales to many small tenants); **schema-per-tenant** when you want per-tenant restore/customization without N databases' connection overhead; **database-per-tenant** for enterprise/compliance (HIPAA/SOC2 data-residency), per-tenant encryption/restore, or one tenant so large it deserves its own resources. **Hybrid pods:** small tenants share a pool, large/enterprise tenants get dedicated DBs — a `tenant → shard/connection` routing map (a "tenant catalog" table in a control-plane DB) decides at request time. Write the decision in an ADR (see write-adr); migrating models later is a large project.

2. **Add `tenant_id` to every tenant-owned table — non-null, indexed, first column of composite indexes.** In the shared model, every table carrying tenant data gets `tenant_id uuid NOT NULL REFERENCES tenant(id)`. Make it the **leading column** of relevant indexes and most composite PKs/uniques (`UNIQUE (tenant_id, email)` not `UNIQUE (email)` — email is unique *per tenant*, not globally). Global/system tables (plans, feature flags, the `tenant` registry itself) have no `tenant_id`. Never let `tenant_id` be nullable or default — a null tenant row is an isolation hole.

3. **Resolve tenant context at the edge, from a trusted source — never from a client-supplied body field.** Map the inbound request to exactly one tenant:

   | Source | How | Note |
   |---|---|---|
   | **Subdomain** | `acme.app.com` → `acme` | Friendly; needs wildcard DNS/TLS; map slug→tenant_id in catalog |
   | **`X-Tenant` header** | API/service-to-service | Trust only if the caller is authenticated; never from a browser unauthenticated |
   | **JWT `org`/`tenant` claim** | from the verified token | **Most trustworthy** — signed, can't be forged client-side |

   Resolve once at the edge (middleware), validate the tenant is active, and store it in an **immutable request context** (not a mutable global). The cardinal rule: derive `tenant_id` from the **authenticated identity**, never from a request body/query param — a client-supplied `tenant_id` is a cross-tenant skeleton key (this is exactly the gap **design-authorization-model** warns about). If subdomain and token disagree, reject.

4. **Defense in depth — app-layer scoping is the primary guard, Postgres RLS is the safety net.** The #1 production multi-tenancy bug is a single query that forgot its tenant filter → cross-tenant leak. You need **both** layers because each fails differently:
   - **App layer (primary):** every query is scoped through a **tenant-aware repository / ORM global filter** so developers physically can't write an unscoped query. Don't rely on each engineer remembering `WHERE tenant_id = $1` — inject it centrally (e.g. an ORM global scope, a base repository that always appends the filter, a query builder that refuses to run without a tenant).
   - **DB layer (backstop):** Postgres Row-Level Security catches the day someone bypasses the repository or writes raw SQL.

   ```sql
   ALTER TABLE document ENABLE ROW LEVEL SECURITY;
   ALTER TABLE document FORCE ROW LEVEL SECURITY;        -- applies to the table owner too
   CREATE POLICY tenant_isolation ON document
     USING       (tenant_id = current_setting('app.tenant_id')::uuid)   -- read/update/delete visibility
     WITH CHECK  (tenant_id = current_setting('app.tenant_id')::uuid);  -- blocks INSERT into another tenant
   ```
   `FORCE` is non-negotiable (without it the table owner — usually your app's role — bypasses RLS). `WITH CHECK` stops a write that *sets* a foreign `tenant_id`. The app role must **not** have `BYPASSRLS`.

5. **Set the RLS variable with `SET LOCAL` inside the transaction — the connection-pool caveat that breaks naive RLS.** RLS reads `current_setting('app.tenant_id')`. You must set it per request — but **how** depends on the pooler:
   - With **PgBouncer in transaction mode** (the common setup), a connection is handed to a *different* tenant's request the instant your transaction commits. A session-level `SET app.tenant_id = ...` therefore **leaks** the previous tenant's value into the next request — a catastrophic cross-tenant bug.
   - Fix: set it **transaction-scoped** so it auto-resets at commit/rollback:
     ```sql
     BEGIN;
     SET LOCAL app.tenant_id = '...';   -- reset automatically at COMMIT/ROLLBACK; never plain SET
     -- ... all queries in this request ...
     COMMIT;
     ```
   - Equivalent: `SELECT set_config('app.tenant_id', $1, true)` (the `true` = local). Every tenant request must run inside a transaction that begins with `SET LOCAL`. Assert in the repository that the var is set before any query runs, so a missing context fails closed (returns zero rows / errors) rather than leaking.

6. **Per-tenant quotas + noisy-neighbor mitigation.** In a shared model one tenant can starve the rest. Enforce **per-tenant rate limits and quotas keyed by `tenant_id`** (token bucket / sliding window — see **rate-limiting**), plus resource guards: statement timeouts, max connections per tenant, row/storage caps, background-job concurrency caps per tenant. For chronic offenders or very-large tenants, move them to a **dedicated pod/DB** (step 1's hybrid). Track per-tenant usage metrics (queries/sec, storage, CPU) so you can detect and isolate a noisy neighbor before it causes an incident.

7. **Tenant offboarding — clean per-tenant export and verifiable hard delete.** Deletion and export are isolation-critical and a GDPR obligation (mechanics: **map-privacy-data-gdpr**):
   - **Export:** dump all rows where `tenant_id = $1` across every table to a machine-readable archive. Database-per-tenant makes this a `pg_dump` of one DB; shared schema requires a tenant-scoped export of every table (drive it from a registry of tenant-owned tables so none is missed).
   - **Hard delete:** in shared schema, `DELETE` cascades by `tenant_id` (rely on `ON DELETE CASCADE` from the `tenant` row, or a deterministic ordered delete) — and don't forget derived data: caches, search indexes, object storage, analytics warehouse, backups' retention policy. Database/schema-per-tenant: `DROP DATABASE`/`DROP SCHEMA` is the cleanest, most auditable erasure. Verify deletion (assert zero rows remain for the tenant) and log it for compliance.

8. **Migrations across thousands of tenants — online, batched, versioned, idempotent.** Schema changes don't break with one model but they *scale* differently:
   - **Shared schema:** one migration changes all tenants at once — fast, but a bad migration's blast radius is everyone. Use online/safe DDL (see **db-migration-safety**: avoid long table locks, backfill in batches, add indexes `CONCURRENTLY`).
   - **Schema-per-tenant / DB-per-tenant:** loop the migration over every schema/database. This must be **batched, resumable, and idempotent** — track each tenant's schema version in the catalog, run N at a time, record success/failure per tenant, and be able to retry only the failures. A 4,000-tenant migration that aborts at tenant 2,500 must resume, not restart. Roll out behind a flag and canary on a few tenants first.

9. **Cache and search keyed by tenant; cross-tenant admin features that don't bypass isolation.**
   - **Caching:** every cache key includes `tenant_id` (`doc:{tenant_id}:{id}`) so tenant A can never read tenant B's cached value, and invalidation can be per-tenant (see **caching-strategy**). Same for search indexes (per-tenant index or a mandatory tenant filter on every query).
   - **Admin / impersonation:** when support impersonates a tenant, **set the same `app.tenant_id` and go through the same scoped path** — don't add a "god query" that ignores RLS. Use a separate, audited DB role with `BYPASSRLS` *only* for narrow platform operations, and **log every impersonation** (build-audit-logging). **Global analytics** (cross-tenant metrics) is the one legitimate cross-tenant read: run it through a dedicated read-only role/replica with explicit tenant aggregation, isolated from the application path — never by relaxing the app's RLS.

10. **Test tenant isolation as a first-class, automated guarantee — the leak test is the one that matters.** Ship these as CI tests, not manual checks:
    - **Cross-tenant denial:** seed data for tenant A and tenant B; with context set to A, assert that *every* read/list/get of B's resources (by real id) returns **zero rows / 404 / deny** — including raw SQL paths, the cache, and search.
    - **RLS backstop:** run a query that *omits* the app-layer filter against a session with `app.tenant_id = A` → still returns only A's rows. Proves the data tier holds when the app forgets.
    - **Fuzz the `tenant_id`:** randomize/swap the tenant in the request context and assert no other tenant's data is ever returned and no write lands in the wrong tenant (`WITH CHECK` holds).
    - **Pool leak test:** run interleaved requests for A then B over a transaction-mode pool and assert B never sees A's `SET LOCAL` value.
    - **Optional per-tenant keys:** if tenants have their own encryption keys (envelope encryption, key per tenant in a KMS), test that the wrong key can't decrypt another tenant's data and that key deletion = crypto-shredded data.

    Done = an isolation model chosen against the tradeoff table and recorded in an ADR; `tenant_id` non-null + indexed on every tenant table (and leading in uniques); tenant context derived from the verified identity at the edge and propagated as immutable request state; every query scoped at the app layer **and** RLS (`FORCE` + `WITH CHECK`, app role without `BYPASSRLS`) enforced, with the var set via `SET LOCAL` per transaction; per-tenant quotas in place; migrations fan out batched/resumable/versioned; export + verified hard delete defined; caches/search/admin/analytics tenant-keyed; and an automated cross-tenant leak test (plus fuzz + pool-leak) passing in CI.
