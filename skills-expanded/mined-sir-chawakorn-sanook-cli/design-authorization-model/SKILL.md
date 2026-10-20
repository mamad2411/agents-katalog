---
name: design-authorization-model
description: Designs an authorization model — RBAC/ABAC/ReBAC, multi-tenant isolation, resource ownership, and policy-as-code (OPA/Cedar/Oso) — keeping authZ decisions separate from authN identity in a centralized, testable policy layer enforced down to the data tier.
when_to_use: A system needs roles/permissions, multi-tenant data isolation, or per-resource access rules beyond a logged-in check. Distinct from auth-jwt-session (who you are — tokens/sessions), security-review (audit), and rate-limiting (request volume).
---

## When to Use

Reach for this skill when the question is **"is this caller allowed to do this to this resource?"** — not "who is this caller?":

- "Add roles and permissions" / "only admins can delete, members can edit, viewers read"
- "Tenants must not see each other's data" / "isolate orgs / workspaces"
- "Owner can share a doc with specific users" (Google-Drive-style) → relationship graph
- "Permissions depend on attributes" — department, resource status, time, region
- "Stop scattering `if user.role == 'admin'` across 40 handlers — centralize it"
- An IDOR/cross-tenant leak found in review (a user fetched another org's record by id)

NOT this skill:
- Issuing/verifying tokens, sessions, refresh rotation, OAuth/OIDC login → **auth-jwt-session** (authN establishes identity; this skill consumes that identity to make the access decision)
- Auditing existing code for access-control holes by severity → **security-review**
- Capping request *rate/volume* per caller → **rate-limiting**
- Recording *who did what when* for compliance/forensics → **build-audit-logging**
- GDPR data-subject rights, lawful basis, PII mapping → **map-privacy-data-gdpr**
- Fixing injection/XSS/SSRF in web code → **remediate-web-vulnerabilities**

## Steps

1. **Pick the model by the shape of the access rule — do not default to RBAC for everything.**

   | Model | Decide by | Use when | Engine fit |
   |---|---|---|---|
   | **RBAC** | role → permission set | Fixed, coarse tiers (admin/editor/viewer); permissions don't depend on the specific row | DB tables, Casbin, Cedar |
   | **ABAC** | attributes of subject+resource+context | Rules vary by field/status/time/region (`owner.dept == doc.dept AND time < embargo`) | **OPA/Rego**, Cedar |
   | **ReBAC** | relationship/ownership graph | Per-resource sharing, nesting (`folder→doc`), "users this owner invited" — Drive/GitHub-style | **OpenFGA / SpiceDB** (Zanzibar), Oso |

   Default: start **RBAC for app-wide roles**, add **ReBAC** the moment you need per-resource sharing or hierarchy, add **ABAC** conditions for field/context rules. They compose — RBAC roles can be relations in a ReBAC graph. Don't roll a bespoke nested-`if` engine; pick one of the named tools.

2. **Separate authN from authZ — the decision is its own layer.** AuthN hands you a verified principal (`{user_id, tenant_id, roles}` from the validated token — see **auth-jwt-session**). AuthZ takes `(principal, action, resource)` → `allow|deny`. Never re-derive identity inside the policy, and never let the policy trust unverified claims.

3. **Centralize the decision behind one `authorize()` call — never inline `if role ==`.** Every protected operation calls the same checkpoint; scattered checks drift and leak.

   ```python
   # ONE entry point. Engine (OPA/Cedar/Oso/OpenFGA) behind it.
   def authorize(principal, action, resource):
       decision = engine.check(
           subject=principal.user_id,
           tenant=principal.tenant_id,      # from token, NEVER from the request body
           action=action,                   # "document:delete"
           resource=resource,               # {id, type, tenant_id, owner_id, status}
       )
       if not decision.allow:               # deny by default — no rule matched = deny
           raise Forbidden(action, resource.id)
       return decision
   ```

4. **Enforce multi-tenant isolation on every query — and derive `tenant_id` from the token, never the client.** A client-supplied tenant/org id is an attacker-controlled cross-tenant key. Scope every read/write by the token's tenant; treat a missing tenant scope as a bug, not a default-all.

   ```sql
   -- Defense in depth: Postgres Row-Level Security so a forgotten WHERE can't leak.
   ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
   ALTER TABLE documents FORCE ROW LEVEL SECURITY;          -- applies to table owner too
   CREATE POLICY tenant_isolation ON documents
     USING (tenant_id = current_setting('app.tenant_id')::uuid);
   ```
   Set `app.tenant_id` per request/connection from the verified token (`SET LOCAL app.tenant_id = ...` inside the request transaction). App-layer `WHERE tenant_id = $1` is the primary guard; RLS is the backstop for the day someone forgets it.

5. **Deny by default, least privilege, deny wins.** No matching allow rule ⇒ deny. Start every role at zero permissions and add. When allow and deny rules overlap, **explicit deny beats allow**. Write this into the policy, don't rely on convention.

6. **Make policy versioned, code-reviewed, and unit-tested — policy-as-code.** Keep `.rego` / Cedar / `policy.polar` in the repo, PR-reviewed like app code. Example OPA/Rego with the three non-negotiables baked in:

   ```rego
   package authz
   default allow := false                          # deny by default
   default deny := false                           # bare `deny` is always defined

   allow if {                                       # owner can do anything to own resource
     input.resource.tenant_id == input.principal.tenant_id   # same-tenant gate, always
     input.resource.owner_id == input.principal.user_id
   }
   allow if {                                       # role grants the action
     input.resource.tenant_id == input.principal.tenant_id
     some role in input.principal.roles
     grants[role][_] == input.action               # e.g. grants.editor[] = "document:edit"
   }
   deny if input.resource.status == "locked"        # explicit deny condition
   final_allow := allow and not deny                # deny wins over any allow
   ```
   Wire the API to read `final_allow`, not `allow`. Run `opa test policy/ -v` in CI. The same input schema feeds both the running engine and the tests.

7. **Pass the decision an explicit resource snapshot, fetched tenant-scoped first.** Load the resource (already filtered by tenant in the query) before checking, so the policy sees real `owner_id`/`status`/`tenant_id`. Checking by id alone, then fetching unscoped, reintroduces the IDOR.

8. **Verify with an allow/deny matrix per role × action — including explicit cross-tenant denial** (see Verify) before shipping.

## Common Errors

- **Trusting a client-supplied `tenant_id`/`org_id`** from body, query, or header. It's the cross-tenant skeleton key. Derive tenant solely from the verified token; ignore any tenant field in the request.
- **IDOR — checking the role but not the ownership/tenant of *this* row.** `can_edit_documents` is true, but the doc belongs to another tenant. Always bind the check to the specific resource's `tenant_id`/`owner_id`, fetched tenant-scoped.
- **Inline `if user.role == 'admin'` scattered across handlers.** They drift, one gets missed, and a new action ships unguarded. Route every check through the single `authorize()` checkpoint.
- **Role explosion (`editor_us_finance_readonly`).** Combinatorial roles that should be attributes. Move per-field/context rules to ABAC conditions; keep roles coarse.
- **Allow-by-default / "fail open."** A request that matches no rule slips through, or an engine error returns allow. Set `default allow := false` and treat engine errors/timeouts as deny.
- **Reading `allow` instead of the deny-wins result.** Exposing `allow` to the API skips the explicit-deny rule. Have the engine return `final_allow` (`allow and not deny`) so a locked/blocked resource can't be reached through a permissive role.
- **AuthZ in the frontend only.** Hiding a button is UX, not security — the API is the enforcement boundary. Every server endpoint authorizes independently.
- **Roles baked into the JWT and never refreshed.** Revoking a role doesn't take effect until the token expires. Check permissions against current state (or keep token TTL short and re-resolve roles server-side).
- **No DB-tier backstop.** One forgotten `WHERE tenant_id` leaks every tenant. Enable Postgres RLS with `FORCE` so the data tier denies even when the app forgets.
- **Confused-deputy / unscoped service calls.** A worker or internal service queries with god privileges on behalf of a user without carrying the user's tenant/permission scope. Propagate the principal; don't let internal callers bypass `authorize()`.
- **Policy with no tests.** Untested Rego/Cedar rots silently. Ship the allow/deny matrix as `opa test` cases alongside the policy.

## Verify

1. **Allow/deny matrix — every role × action.** For each role (admin/editor/viewer/none) × each action (create/read/update/delete/share), assert the decision matches the intended table. Every cell is a test case, run in CI (`opa test policy/ -v` or the engine's harness).
2. **Cross-tenant denial (the critical one).** User in tenant A requests a resource in tenant B by its real id → **403/deny**, for *every* action, including read. Do this both through the API and by querying the DB with `app.tenant_id` set to A — RLS must return zero rows.
3. **IDOR probe.** As a non-owner same-tenant user, attempt update/delete on a resource you don't own and your role doesn't permit → deny. Then as owner → allow. Confirms the check binds to the resource, not just the role.
4. **Deny by default.** Invent a brand-new action string with no policy rule → deny (not allow). Proves nothing slips through unmatched.
5. **Deny wins.** A resource in `status = "locked"` (or a user under an explicit deny) → deny even when a role would otherwise allow. Assert against `final_allow`, the value the API consumes.
6. **RLS backstop.** Run a `SELECT` that *omits* the app-layer tenant filter against a session with `app.tenant_id` set → still returns only that tenant's rows. Proves the data tier holds when the app forgets.
7. **Centralization.** `grep -rnE 'role *== *|isAdmin|\.role\b' src/` finds zero authorization branches outside the policy layer — every decision goes through `authorize()`.
8. **Privilege escalation negative test.** A user cannot grant themselves a role/permission or modify a policy they shouldn't (the "edit roles" action is itself authorized).

Done = the role × action matrix passes in CI, cross-tenant and IDOR probes are denied at both the API and DB tier (RLS enforced), the policy is versioned with `default allow := false` and deny-wins (API reads `final_allow`), and `grep` finds no authorization logic outside the centralized layer.
