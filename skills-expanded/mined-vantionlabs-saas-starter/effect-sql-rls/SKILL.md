---
name: effect-sql-rls
description: Use when writing any query, migration, or test that touches tenant data in this repository. Covers withOrgScope and withWorkerScope, the two Postgres roles and why the boundary is in the database rather than in a lint rule, the shape a row-level security policy has to take, when Effect.orDie is right, and why a fixture seeds through the product's own write path.
---

# Tenant data, and the two things that keep it apart

Every tenant-owned table is protected **twice**: a row-level security policy in Postgres,
and `withOrgScope` around the query. Neither is trusted alone. Unit tests cover each; only
`e2e/tests/tenancy.spec.ts` shows two real users, session to SQL, failing to see each
other's rows.

## The connection is the boundary

`packages/database/src/roles/init.sql` makes two roles:

- **`vantion`** — what every application process connects as, and `NOBYPASSRLS`. A handler
  that forgets `withOrgScope` therefore reads **nothing** rather than reading everybody.
- **`admin`** — holds `BYPASSRLS`, for the cross-tenant surface only. Which process may
  cross tenants is decided by Postgres, not by a reviewer.

This was not true until recently. `docker compose` set `POSTGRES_USER: vantion`, making it
the bootstrap **superuser** — so every policy in this schema was inert while
`pg_class.relrowsecurity` read true. `packages/database/test/Role.test.ts` asserts the
connection cannot bypass, because a suite pointed at a superuser passes every tenancy test
while proving nothing.

Switching the role found two production bugs, both the same shape: a worker escape on
`using` but not on `with check`, and an UPDATE is checked by both.

## Which scope

| Function                    | Who uses it                                        | What it sets                         |
| --------------------------- | -------------------------------------------------- | ------------------------------------ |
| `withOrgScope`              | A handler with a caller                            | `app.current_org` from `CurrentUser` |
| `withOrgScopeFor(orgId, …)` | A seed, a test, anything with an id and no session | the same, from a plain id            |
| `withWorkerScope`           | The relay, delivery, the Stripe webhook            | `app.worker = 'on'`                  |

`withOrgScopeFor` lives in `packages/database` and `withOrgScope` in
`@vantion/module-iam`, because reading the caller is an identity concern and `database`
would otherwise depend on the module that depends on it.

**Filter by organization _and_ scope.** Both, never either. `currentSubscription` relied on
the policy alone and every organization read the first subscription row in the table — a
superuser, or any role with BYPASSRLS, ignores row-level security even on a FORCEd table,
which is what a managed Postgres often hands you.

## Writing a policy

Split by command rather than widening one. `0012_worker_writes.sql` is the worked example:
INSERT stays exactly as strict as it was, and the worker gains only the ability to update
what it is already allowed to read.

```sql
create policy "x_select" on "x" for select
  using ("organizationId" = current_setting('app.current_org', true)
         or current_setting('app.worker', true) = 'on');

create policy "x_insert" on "x" for insert
  with check ("organizationId" = current_setting('app.current_org', true));
```

A table better-auth owns gets **no policy at all** rather than a permissive one — see the
`better-auth` skill and `0011_sso.sql`.

## `Effect.orDie` on a query is usually right

`RULES.md` says when. What reaches an `orDie` on a `sql` call is the database being
unreachable, the query being wrong, or a policy refusing it — all bugs. The durable rule:
**adding a constraint to a table is the moment to revisit every `orDie` writing to it**,
because that is when a defect becomes a message somebody needed.

## Tests seed through the product's write path

Not because it is tidy, but because a fixture needing more privilege than the application
has is a fixture describing a state the application cannot produce. Use `withOrgScopeFor`,
not a bare insert — a bare insert into a policied table is refused outright.

Database-backed tests skip without a database. `describe.skipIf(testDbUrl() === undefined)`.

## Where to look

- `packages/database/src/OrgScope.ts`, `packages/modules/iam/src/identity/OrgScope.ts`
- `packages/database/src/migrations/0002_rls.sql`, `0012_worker_writes.sql`
- `packages/database/test/Role.test.ts` — the test that keeps the role honest
- `packages/modules/admin/` — the only thing using the second role, through `crossTenant`
