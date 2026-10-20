---
name: saas-multitenancy
description: Tenant isolation implementation specialist. Auto-invoked when tenant boundary code is written — row-level security (RLS) policies, query guards, tenant context propagation middleware, cross-tenant access checks, or partition-key enforcement. Also invoked when noisy-neighbor or per-tenant quota code is being added.
---

# SaaS Multitenancy

Cross-tenant data leaks should be structurally impossible, not merely unlikely —
one leaked row is a breach disclosure, not a bug ticket. The second goal is
keeping the isolation layer from becoming a performance tax.

## When to reach for this

- Writing or reviewing RLS policies, ORM tenant guards, or query-builder hooks
- Building tenant-context propagation (middleware, async boundaries, job workers)
- Adding per-tenant quotas, rate limits, or noisy-neighbor mitigation
- Auditing cross-tenant access paths: admin tools, support impersonation, caches

## Principles

1. **Assume the worst tenant.** Design as if one tenant is actively trying to read
   another's data. Every query without a tenant filter is a bug, not a TODO.
2. **Defense in depth.** RLS is the last line, not the only line — application-layer
   guards, per-request context binding, and negative tests all belong simultaneously.
3. **Fail closed.** Missing tenant context refuses the request. An unset session
   variable must yield zero rows, never "default to public."
4. **Trust nothing from the client.** Tenant ID comes from the authenticated
   session, never from a request parameter, header, or body field the client controls.
5. **Background jobs are the common leak path.** Queue workers, scheduled jobs,
   cache refreshers, and analytics pipelines drop tenant context far more often
   than request handlers do. Audit them explicitly; make job payloads carry the
   tenant ID and re-bind context per job.
6. **Prove isolation with tests, not reasoning.** Every guarantee gets a negative
   test that attempts the forbidden access and asserts zero rows / explicit denial.
7. **Measure the tax.** RLS predicates and per-tenant quotas have a cost — typically
   small when the tenant column leads the index, painful when it doesn't. Benchmark
   before and after; surface the overhead in the ADR.

## RLS skeleton (Postgres)

The load-bearing shape — full policy set, role setup, pooling caveats, and the
negative-test suite are in [`references/rls-policies.md`](references/rls-policies.md):

```sql
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects FORCE ROW LEVEL SECURITY;  -- applies to the table owner too

CREATE POLICY tenant_isolation ON projects
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
-- per request/job, inside the transaction:
--   SET LOCAL app.tenant_id = '<uuid from the authenticated session>';
```

Two details carry the guarantee: the app connects as a **non-superuser, non-owner
role** (superusers and `BYPASSRLS` roles skip RLS silently), and `SET LOCAL` is
used with transaction-mode pooling so context can never leak across pooled
connections.

## Pitfalls

- App connecting as the table owner or a superuser — RLS silently bypassed unless
  `FORCE ROW LEVEL SECURITY` is set (and never bypassable for superusers)
- `SET` instead of `SET LOCAL` with a connection pooler — tenant context bleeds
  into the next request on that connection
- Cache keys without the tenant ID — the second tenant gets the first tenant's data
- Unique indexes and sequences that are global when they should be per-tenant
  (cross-tenant existence leaks via duplicate-key errors)
- Admin/support tooling that disables guards instead of using an audited
  impersonation path with actor + target + reason logged
- Isolation verified only through request handlers, while background jobs and
  raw-SQL reporting queries go untested

---
*Related: `saas-data-model` (tenant-leading indexes, partitioning),
`saas-auth-sso` (where tenant context originates), `saas-collab-sync` (channel
isolation) · domain agent: `saas-architect` (pooled/bridge/silo choice) ·
output/ADR format: `playbook-conventions`*
