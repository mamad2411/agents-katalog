---
name: rls-policy
description: Enforce authorization at the DATA layer and prove it — deny by default, one rule per operation per principal, and an EXECUTED allow test plus an EXECUTED deny test for every principal. Covers row-level security, repository-layer tenant predicates, policy engines, and document rules. Use whenever a table/collection holds user/tenant/PII/payment/health data, when changing who can read or write what, or when a review flags missing authorization. Trigger words — authorization, RLS, row-level security, policy, allow/deny, deny test, tenant isolation, multi-tenant, access control, permission matrix, pgTAP.
---
# Data-layer authorization (+ executed allow/deny tests)

**Use when:** any table, collection, bucket or keyspace holds user/tenant/PII/payment/health data, or a
change moves who may read or write what. **Owners:** security-engineer (final gate), database-architect.
*RLS is the Postgres name for a control every datastore needs some form of* — the contract below is the
control; the mechanism that carries it depends on your stack.

## The contract
- **Authorization is enforced at the DATA layer**, not only at the UI or the endpoint. The UI hiding a
  control is not a control, and an endpoint check is the second line, never the only one.
- **Deny by default.** A new table/collection is unreadable and unwritable until a rule says otherwise.
- **Every rule ships with an EXECUTED allow test AND an EXECUTED deny test**, for every relevant principal.
  A deny that was never run is a deny that does not exist.
- **The privileged/service credential never travels on a user request path.** Where a trusted path genuinely
  needs it, it carries a guard and writes an audit row.

## Inputs
The table/collection + its ownership or tenancy edge (who owns a row, which org/cohort/tenant scopes it),
the role set, and the intended permission matrix (read/write per role) from `docs/security/security-model.md`.

## Procedure
1. **Restate the matrix in one line** — read `docs/security/security-model.md` and the project's policy doc,
   then write who may read / create / update / delete this data, as which principal. Ambiguity resolves to deny.
2. **Turn on deny-by-default in the SAME change as the schema.** No rule ⇒ no access. Shipping the schema
   first and the rules later means the data is readable in between, and "later" is where the breach lives.
3. **Write one rule per operation per principal**, expressed with the project's ownership/tenancy predicate
   (`owns_row`, `in_tenant(scope)`, `is_staff_of(scope)`, `is_admin`). Reuse the shared predicate — a rule
   that re-implements the tenancy check is a rule that will drift from it.
4. **Field-level secrets** (tokens, internal notes, provider refs, host URLs) do not belong in a column
   exception: isolate them into a sidecar table/collection with no read rule, or expose only an allowed-field
   projection/view that runs as the caller.
5. **Trusted path, explicitly.** If a job, webhook or admin task must bypass the rules, name it in the docs,
   guard it, and require an **audit row** — never widen a rule to accommodate it.
6. **Write the allow AND deny tests** in the same PR, one assertion per principal:
   **owner ✓ · other-tenant ✗ · assigned-staff ✓ · unassigned-staff ✗ · admin ✓ · anonymous ✗.**
   Each test authenticates as that principal against the real datastore — not a mocked client.
7. **Run them until green**, then update `docs/specs/data-model.md` and the policy doc if the pattern is new.
8. **Verify:** run `scripts/verify.sh`, then run the **allow test AND the deny test** against the migrated
   datastore and record both with `scripts/verify.sh --observe "<expected>" "<observed>"` — quote the test
   names and their results (owner ✓ · other-tenant ✗ · anon ✗).
9. **Promote the deny test to `vantry.yml` `acceptance:`** so it re-runs on every verification forever. A
   regression six months from now then blocks the push of someone who never heard of this table.

## When the datastore has no row-level security
The contract does not change — only where it is enforced. In every case, proven by the same executed pair.
- **Relational without RLS** (MySQL, SQLite, most ORMs): the **query/repository layer**, with a **mandatory
  tenant/owner predicate** injected in ONE place that no caller can bypass. Add a test that fails on a raw
  query built outside it — an optional predicate is not a control.
- **Document rules engines** (Firestore, Realtime Database): the **rules file** is the policy; deny at the
  root and grant downward. Rules are code: they get the same allow/deny tests.
- **Key-value / wide-column** (DynamoDB, Redis): the **partition/key prefix IS the boundary** — tenant id
  leads the key, and the credential's policy conditions it to that prefix.
- **Service-layer architectures**: the service is the data layer. Every handler passes through a single
  `authorize(principal, action, resource)` call or a **policy engine**; the datastore accepts the service
  and nothing else, and the service trusts nobody.

## Guardrails
- Sensitive data without deny-by-default **and** a passing executed allow/deny test is not done — block the PR.
- Never use a privileged/service credential on the user path to "make it work" — fix the rule.
- Prefer denying over leaking when a rule is ambiguous.
- This is authorization: the path lands in `vantry.yml` `sensitive_paths`, so the PR cannot merge without a
  committed `.vantry/reviews/<branch-slug>.security.json` with `verdict: pass`.

## Done when
Deny-by-default is on; rules match the matrix; docs updated; a **fresh passing receipt** for this branch whose
observation quotes the **allow and deny** test names and both results; the deny test is listed under
`vantry.yml` `acceptance:`; `scripts/verify.sh` passes and CI re-runs the same contract; a committed security
review with `verdict: pass` confirming intent = rule.

## The vendored Postgres reference does not replace this playbook
**`vendor/skills/supabase-postgres/`** is worth reading for `(select auth.uid())` wrapping and policy
performance. It is **not** a substitute for anything below: upstream advertised "RLS policies and the tests
that verify them" and ships **zero tests**, and it presents an unguarded `current_setting('app.current_user_id')`
GUC pattern as correct. `CONFLICTS.md` beside it gives the fail-closed form.

The requirement here is unchanged: the policy, an **executed** allow test and an **executed** deny test in the
same change, and the deny test promoted to `acceptance:`.

## The identity you test with must be the identity the app uses
This is the strongest playbook in the security set — the six-principal matrix really is mutation-sensitive, and
promoting the deny test to `acceptance:` is the only durable re-run guarantee here. It has one hole, the same
shape as audit-log's: **the matrix never runs on the connection the application opens.**

Row security does not apply to a table's **owner** or to a superuser unless it is forced. A matrix that is green
as `test_user` therefore says nothing about an app whose `DATABASE_URL` is the owner — and in that configuration
the app reads every tenant's rows while all six assertions pass.

Two requirements, and they are contract, not illustration:
- The application connects as a **non-owner, non-superuser role**. Assert it: run `SELECT current_user` on the
  app's own connection and record the answer in `--observe`.
- Row security is **forced for the owner too**, wherever the engine supports it (in Postgres,
  `ALTER TABLE <t> FORCE ROW LEVEL SECURITY`). Without it one careless `DATABASE_URL` disables every policy in
  the schema, silently.

That second requirement previously lived only inside the Stack notes block below — which this playbook itself
declares **void** for any other stack. A control that disappears when you change database is not a control.

## Stack notes — PostgreSQL + Supabase (illustration, not contract)
If `vantry.yml` `stack:` names something else, this section is void and the Procedure above still applies.
- Deny by default = `ALTER TABLE t ENABLE ROW LEVEL SECURITY;` **and** `ALTER TABLE t FORCE ROW LEVEL
  SECURITY;` in the same migration as the table. `ENABLE` alone still exempts the table owner.
- Predicates: `auth.uid()` on Supabase; `current_setting('request.jwt.claims')` or `SET LOCAL role` per
  transaction elsewhere. Wrap reusable checks as `SECURITY DEFINER STABLE` functions with a pinned `search_path`.
- Field-level secrets: a sidecar table with no policy, or a `security_invoker` view of the allowed columns.
- Tests: **pgTAP**, setting `request.jwt.claims` per principal, one `ok()`/`throws_ok()` per row of the matrix.
- The privileged credential is `service_role`: server-only, never imported into a component.
