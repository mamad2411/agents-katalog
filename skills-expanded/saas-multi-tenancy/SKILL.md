---
name: saas-multi-tenancy
description: Tenant isolation and lifecycle for multi-tenant SaaS — data scoping that fails closed, tenant context propagation, noisy neighbors, per-tenant operations. Use when building B2B/B2C SaaS with multiple customers on shared infrastructure, adding tenant-scoped tables or features, debugging cross-tenant data leaks, or when the user says "multi-tenant", "tenant isolation", "SaaS", "workspace", "organization data", or "row-level security".
---

# SaaS Multi-Tenancy

In a multi-tenant system, the worst bug class isn't downtime — it's **tenant A seeing tenant B's data**. One leaked invoice ends the customer relationship and possibly the company. Design so that isolation failures are structurally impossible, not just carefully avoided, because "carefully" doesn't survive the 400th endpoint.

## Choosing the isolation model (decide once, explicitly)

- **Shared schema + `tenant_id` column** — the default. Cheapest to operate, easiest to migrate, scales to thousands of tenants. Requires the discipline below.
- **Schema-per-tenant / database-per-tenant** — buy isolation with operational pain (N× migrations, connection management, cost). Justified by: hard compliance walls, wildly divergent tenant sizes, or contractual "your data is physically separate". Don't drift here for comfort.
- Hybrid (big tenants carved out) is legitimate — but only after the shared model measurably strains.

The rest of this skill assumes shared-schema, where the discipline matters most.

## Gate 1: Scoping that fails CLOSED

The core principle: **a forgotten WHERE clause must return nothing, not everything.**

- Two layers, always: application-level scoping (every query goes through a tenant-scoped session/repository that injects `tenant_id` — never hand-written per query) AND database-level enforcement (Postgres RLS with `FORCE`, policies keyed off a per-request setting, app connecting as a role that **cannot bypass RLS** — superusers silently bypass it; verify the role, and boot-guard against misconfiguration).
- `tenant_id NOT NULL` on every tenant table + FK to the tenants table + composite indexes leading with it (database-design). New tenant-scoped table = added to the RLS/policy list in the same migration, enforced by convention *and* a test that scans the schema for unpoliced tables.
- The tenant comes from the **authenticated principal, never from the request** — no `?account_id=` params, no tenant in the POST body, no trusting a JWT claim you didn't issue (threat-model-security Gate 1).

## Gate 2: Context propagation — where leaks actually happen

Request handlers are the easy part. Cross-tenant leaks live in the places that don't have a request:

- **Background jobs**: every enqueued job carries its `tenant_id` explicitly, and the worker re-establishes tenant context before touching data. A worker processing a loop of tenants must reset context per iteration — context bleeding between loop iterations is the classic leak.
- **Caches**: every cache key of tenant-scoped data includes the tenant (system-design). Query caches cleared on login/logout — stale cross-account data in an SPA is this bug wearing a frontend costume.
- **Scheduled/cron jobs, exports, report generators, search indexes, LLM/RAG retrieval** (ai-engineering): each is a query path; each gets the same scoping audit as an endpoint.
- **Logs and error trackers**: tag entries with tenant (great for debugging) but treat aggregated views as cross-tenant data needing admin-level access.

## Gate 3: The two-tenant test — the cheapest breach prevention that exists

In your test suite, permanently: seed tenant A and tenant B, then as A's user attempt to read, update, delete, and *list* B's objects on **every resource type** — expecting 404/empty, never data. Add the list-endpoint case explicitly (unscoped lists leak in bulk). Run it in CI; every new resource joins it. Before any launch, run it live against production-like data (release-readiness Gate 2). This one fixture catches the bug class that code review misses.

## Gate 4: Tenant lifecycle is a feature set, not an afterthought

Design these before the first real customer, because retrofitting them is surgery:
- **Provisioning**: idempotent tenant creation (seed data, defaults, numbering sequences) — one function, tested.
- **Suspension** (unpaid/abusive): a `blocked`/`suspended` flag checked at auth time, gating the whole app — data preserved, access stopped, reversible.
- **Export**: a tenant can get their data out (their invoices, parties, ledgers) in a usable format. Contractually expected; also your data-privacy-compliance obligation.
- **Purge**: hard deletion of a departed tenant — everywhere: rows, files/objects, search indexes, caches, backups-policy documented. An orphaned tenant's data is pure liability. Purge is destructive: confirm, audit, and stage it (soft-delete window → hard purge).

## Gate 5: Tenants are not the same size — plan for the whale

- **Noisy neighbor**: per-tenant rate limits on expensive endpoints, caps/pagination on unbounded queries (that one tenant with 500k products will find your missing LIMIT), and background-job queues that can't be monopolized by one tenant's bulk import (fair scheduling or per-tenant concurrency caps).
- **Observe per-tenant**: your metrics need a tenant dimension on the hot paths — "the API is slow" vs "tenant 4 is running 80% of load" are different incidents (observability-readiness).
- Per-tenant configuration (features, limits, branding) lives in a tenants/settings table read at runtime — never in code branches naming specific customers.

## Cross-tenant admin operations

Your own admin/support panel is deliberately cross-tenant — which makes it the highest-privilege attack surface you own: separate principal type and stronger auth, every cross-tenant read/write written to an append-only audit log (*who viewed which tenant's what, when*), and impersonation (log-in-as-tenant), if built, is time-boxed, visibly flagged in the UI, and audited. Support convenience is how breaches get built with good intentions.
