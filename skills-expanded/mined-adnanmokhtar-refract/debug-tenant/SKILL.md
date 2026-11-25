---
name: debug-tenant
description: Debug tenant isolation issues — a user sees data that doesn't belong to them, or doesn't see data that does. Use on a suspected cross-tenant leak or a missing-data report; walks the full tenant-resolution chain hop by hop. Not a static scan — it reproduces against a running system via `log-tail-method` and `endpoint-test-method`.
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# debug-tenant

## Premise

Find the real leak, not a plausible one. Every step cites the actual value observed (header, resolved id, session GUC, connection, SQL, cache key) at `<file:line>`. "Probably the cache" is not a root cause. Tenant leaks are security incidents and the report must name the file:line — or the session state — that produced the leaked SQL or cache key.

**There is no single chain. There are four, and Step 0 picks which one you walk.** Application-level filtering, Postgres RLS, schema-per-tenant and database-per-tenant fail in entirely different places, and the verdict that is correct for one is a false positive on the others — most sharply, "the SQL has no tenant filter" is *the bug* under app-level filtering and *the expected shape* under RLS. Walk the selected chain top-to-bottom; skipping a hop on a guess is forbidden.

A "fixed" leak without a regression test that would have caught it is unfinished work.

## When to invoke

- Customer reports: "I see products I don't own" / "my orders are missing"
- Audit finds cross-tenant data in a response
- Cache returns data from tenant B to tenant A

## Steps

### 0. Identify the isolation mechanism — before anything else

The rest of this playbook branches here. Establish which mechanism this project uses (one grep each; a project may use more than one, in which case walk each):

| Mechanism | How to confirm it | Chain to walk |
|---|---|---|
| **Application-level filtering** | a repository base class / query scope injecting `tenant_id` (`grep -rn "tenant_id" <repo-base-class>`); no `ENABLE ROW LEVEL SECURITY` in migrations | Step 1 → 2 → 3A → 3C → 4 → 5 |
| **Postgres RLS** | `ENABLE ROW LEVEL SECURITY` / `CREATE POLICY` in migrations; a `SET LOCAL` or `set_config('app.tenant_id', …, true)` in a request hook | Step 1 → 2 → 3B → 3C → 4 → 5 |
| **Schema-per-tenant** | a per-request `SET search_path` / schema switch; migrations run per schema | Step 1 → 2 → 3C → 3D → 4 → 5 |
| **Database-per-tenant** | connection string / pool selected per tenant at request time | Step 1 → 2 → 3C → 3D → 4 → 5 |

**Halt if this step is skipped.** A chain walked for the wrong mechanism produces a confident false positive — and on a tenant-leak incident a confident wrong answer costs more than no answer.

### 1. Reproduce
- Get the request: correlation id + tenant id + user id + endpoint.
- If reproducible in staging, continue. If not, pull logs.

### 2. Trace tenant resolution
Walk the chain — each step shows what was passed vs what was expected:

```
Request arrives:
  Host:              <header>        → resolved to tenant? <id or NULL>
  X-Product-Id:      <header>        → override applied? <yes/no>
  X-API-Key:         <header>        → resolved to tenant? <id or NULL>
  Domain:            <domain>        → matched tenants.domain? <id or NULL>

TenantResolutionMiddleware:
  Resolved tenant:   <id>
  Written to:        AsyncLocalStorage ✓
```

### 3A. Trace query scope — application-level filtering
For the endpoint that leaked:

```
Controller:  reads TenantContext.get() → <id> ✓
Service:     does NOT pass tenantId around ✓
Repository:  base class adds WHERE tenant_id = :tenantId ✓
Actual SQL:  [dump the query] → does it have tenant_id filter?
```

If the SQL lacks the filter — that's the bug. **This verdict is valid ONLY under application-level filtering.** Under RLS the SQL is *supposed* to carry no filter; asserting the bug here on an RLS project is the most common wrong answer this playbook can give.

### 3B. Trace query scope — Postgres RLS

The SQL carrying no `tenant_id` predicate is correct here. The leak is in the session state, the role, or the policy — walk all five, in order, and record the observed value for each:

```
1. Was the GUC set in THIS transaction?
     SELECT current_setting('app.tenant_id', true);        -- run inside the same tx
     NULL → default-deny: policies comparing to NULL match no rows.
     Symptom is MISSING DATA, not a leak. Root cause: the request hook
     never ran, or it ran on a different connection (→ step 3C).
2. Was it set with SET LOCAL / set_config(..., true) — transaction-scoped —
   or a bare SET — session-scoped?
     A session-scoped SET survives into whatever the pooler hands out next.
     `is_local = true` confines it to the current transaction (Postgres docs,
     `set_config`); that is the only safe form behind a pooler.
3. Which ROLE is the query running as?
     SELECT current_user, rolbypassrls FROM pg_roles WHERE rolname = current_user;
     Superusers and roles with BYPASSRLS always bypass RLS. **Table owners
     normally bypass it too** unless the table carries FORCE ROW LEVEL SECURITY
     (Postgres docs, ddl-rowsecurity). An app connecting as the table owner is
     the classic silent no-op: RLS is "enabled", policies exist, and nothing is
     enforced. This is a LEAK, and it is invisible from the SQL.
4. Is RLS actually enabled on the leaking table, and is there a policy for THIS command?
     SELECT relname, relrowsecurity, relforcerowsecurity FROM pg_class
       WHERE relname = '<table>';
     SELECT polname, polcmd, pg_get_expr(polqual, polrelid)   AS using_expr,
            pg_get_expr(polwithcheck, polrelid)               AS check_expr
       FROM pg_policy WHERE polrelid = '<table>'::regclass;
     relrowsecurity = false → not enabled: every row is visible. LEAK.
     A SELECT-only policy on a table with no ALL/UPDATE policy → default-deny for
     the other commands (missing data), never a leak: with RLS on and no matching
     policy, no rows are visible or modifiable (Postgres docs, ddl-rowsecurity).
5. Does the write policy allow writing rows INTO another tenant?
     Omitting WITH CHECK is safe — Postgres reuses the USING expression for the
     check (docs, ddl-rowsecurity). An explicit permissive `WITH CHECK (true)` is
     not: it lets an UPDATE move a row across tenants. Read check_expr above.
```

Cite the observed value for every numbered line. "RLS is on" is not an observation; `relrowsecurity = t, current_user = app_owner, rolbypassrls = f, FORCE = f` is.

### 3C. Trace the connection — the hop that survives code review

**Between "context" and "repo" there is a hop the chain used to omit: which connection served this query, and was its session state reset since the previous tenant used it.** This is the tenant leak that no amount of reading the repository will find, because the repository is correct.

```
Pool:            <pool name / DSN>  size=<n>
Acquired:        BEFORE or AFTER the tenant context / GUC was set?   ← the whole question
Pooler present:  none | pgbouncer | RDS Proxy | ProxySQL
Pooler mode:     session | transaction | statement
Reset on return: does the pooler / driver RESET session state between checkouts?
```

Failure modes, in the order they actually occur:
- **Connection acquired before the context was set.** The GUC (or `search_path`, or the per-tenant DSN) was applied to a *different* connection than the one that ran the query. Symptom: intermittent — correct under low concurrency, wrong under load.
- **Session-scoped state behind a transaction-mode pooler.** In transaction mode the backend is handed to another client at commit; session state set outside a transaction does not travel with the caller. The pack's own `connection-pooling` pattern names `SET` / `LISTEN` / temp tables as the classic silent break under `pool_mode = transaction`. Fix is `SET LOCAL` inside the transaction, or session mode.
- **Connection returned to the pool without a reset**, then reused by another tenant with the previous tenant's state still on it. This is the leak that looks like nothing in the diff.
- **Schema-per-tenant / database-per-tenant:** the same failure wearing a different hat — a pooled connection still pointing at the previous tenant's `search_path` or database. Verify with `SELECT current_schema(), current_database()` on the leaking query's own connection, not on a fresh one.

### 3D. Trace the namespace — schema-per-tenant / database-per-tenant

```
Resolved tenant:   <id>
Expected schema / database:  <name>
Observed on the query's connection:
     SELECT current_schema(), current_database(), current_setting('search_path');
Migrations applied to this schema?   <yes/no — a missing table falls back to a shared one on some search_paths>
```

A `search_path` containing a shared/public schema **after** the tenant schema is a silent cross-tenant read whenever the tenant schema lacks the table. Report the full `search_path`, not just the first entry.

### 4. Trace cache
If the response was cached:

```
Cache key:  tenant:<id>:<namespace>:<key> ✓  OR  <namespace>:<key> ← LEAK
```

If key isn't tenant-prefixed → that's the bug.

### 5. Event replay
If the data came from an event handler:

```
Event received:      pattern=<x>  metadata.tenant=<id>  payload=<ids>
Handler scoped to:   TenantContext.run(metadata.tenant, ...) ✓
Downstream query:    WHERE tenant_id = :tenantId ✓
```

## Output

```
TENANT LEAK — ROOT CAUSE IDENTIFIED

Request:       GET /reports/daily  tenant=A  correlation=abc-123
Leaked data:   3 orders from tenant B

Root cause:
  src/modules/reports/infrastructure/reports.repository.impl.ts:84
  Raw SQL bypasses base repo:
    SELECT * FROM orders WHERE created_at >= $1
  Missing:
    AND tenant_id = $2

Fix:
  Use this.scope(qb) OR add explicit tenant filter to raw query.

Similar bugs to check:
  grep "SELECT .* FROM orders" src/modules/reports/**/*.ts
```

## Rules

- Never paper over with a "temporary fix" — tenant leaks are security incidents.
- File an incident write-up in `ai/audits/` after root cause is known.
- Add a regression test that would have caught this BEFORE shipping the fix.

## Related

- `.claude/skills/log-tail-method/SKILL.md` — the tracing primitive for steps 2–5: filter by correlation id / tenant id to observe the resolved id, SQL, and cache key at each hop.
- `.claude/skills/endpoint-test-method/SKILL.md` — reproduces the leak deterministically (case 4, wrong tenant) and confirms the fix; a cross-tenant 200 there is the same finding.
- Used by `@bug-investigator` — this playbook is the tenant-isolation branch of that agent's root-cause search.
- `ai/patterns/multi-tenancy.md` — the tenant-resolution + query-scoping contract the application-level chain walks; it also names Postgres RLS with a per-request `SET app.tenant_id` as the stronger belt-and-suspenders, which is the mechanism Step 3B covers.
- `ai/patterns/connection-pooling.md` (database pack — if installed) — pooler modes and the transaction-mode / session-state break behind Step 3C. Not installed → the four failure modes in 3C are self-contained; walk them from the pool config directly.
- `ai/patterns/caching-strategy.md` — the tenant-prefixed, versioned cache-key rule whose violation is the step-4 leak.
- `.claude/rules/backend-principles.md` — the tenant-isolation MUSTs behind "a leak is a security incident".

## Halt conditions

- Halt on hand-waves: every root-cause claim must cite `<file:line>` + the actual SQL or cache key produced.
- Halt if Step 0 was skipped, or if the chain walked does not match the mechanism Step 0 identified — a chain walked for the wrong mechanism produces a confident false positive.
- Halt if a hop in the selected chain was skipped without a recorded reason.
- Halt on an RLS project if the report concludes from the SQL alone. The five RLS observations (GUC value in-transaction, `SET LOCAL` vs `SET`, `current_user` + `rolbypassrls`, `relrowsecurity` + `relforcerowsecurity` + the policy rows, and the write policy's `WITH CHECK`) are each required, with the observed value quoted.
- Halt if the connection hop (3C) was not answered: which connection served the query, and whether its session state was reset since the previous tenant used it.
- Halt if the fix ships without a regression test that fails on the unfixed code path.
- Halt if the incident write-up is deferred — `ai/audits/` entry is part of "done", not an after-task.
