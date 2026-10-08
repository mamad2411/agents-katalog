---
name: permdock-audit
description: Reviews an existing PermDock setup or a pull request that changes it. Use when auditing permissions, reviewing a PR that touches permissions.ts, policy.ts or an adapter guard, finding ungranted or unused leaves, missing human approvals on agent tools, closures that should be portable, validate never, untested grants, or mapping an app to OWASP ASI02 and ASI03. Use whenever the user asks to audit, review or harden PermDock.
license: MIT
metadata:
  author: ScaleDockHQ
  homepage: https://permdock.dev/docs/for-ai-agents
  repository: https://github.com/ScaleDockHQ/permdock
---

# Audit PermDock

Read the app's `permissions.ts`, `policy.ts`, factory file and every adapter guard, then write the findings as a Markdown checklist the user can turn into pull requests. Every finding names the file and the permission or role.

## Inputs (find out, or ask before starting)

- The scope: the whole app, or one pull request against its base branch.
- Whether the `permdock` binary runs here (`permdock usage --json`, `permdock doctor --json`); otherwise walk the files and the catalog by hand.
- Which topic areas the app uses: agent runtimes, approvals, named scopes and custom roles, ORM queries or RLS, tokens, API keys or share links.

## Invariants

1. Report, never fix silently. Each finding is one line with a file and a permission or role.
2. Anything that widens access or fails open leads the report.
3. Expected outcomes in tests are written by hand, never computed by calling `decide` or `can`.
4. A topic skill's Verify list is the checklist for its area; this skill does not repeat it.

## Workflow

1. **Inventory.** List every leaf from `definePermissions`, every role from `defineRoles` / `role()`, every plan from `definePlans`, and every grant from `definePolicy` (`grants`, role bindings, `delegations`). Note which entries import the policy (server, agent) and which import only the snapshot (client).
   ✓ Every leaf, role, plan and grant is in the report, including leaves with zero grants.
2. **Ungranted and unused.** A leaf no `allow` mentions is ungranted: grant it or delete it. A granted leaf never passed to `can`, `decide`, `assert`, `protect`, `tools` or `<Protected>` is unused; confirm with `usage --json` or a repo-wide search for the reference.
   ✓ Every leaf is tagged granted and used, granted and unused, or ungranted.
3. **Validation and identity.**
   - `validate: 'never'` on a policy that sees HTTP bodies, MCP arguments or model output is a finding.
   - Client entries (`permdock/react` and the client half of a framework adapter) import permissions and snapshots only.
   - `subject` and `actor` come from the host session or `subjectFrom*`, never from tool arguments or a model-supplied id.
   - A `limit` grant without `limits` on `createPermDock` always denies with `limit-unavailable`, and a mutation that only calls `can` never spends a unit.
   - On Supabase, every `ctx.supabaseAdmin`, `withPostgresAdminClient` or `service_role` client sits behind `permdock.assert(...)` (or `withPermDock({ protect })`), and `subjectFromSupabase` receives `getClaims()` output or `ctx.jwtClaims`, never `getSession().access_token` or `user_metadata`.
     ✓ Each check has a pass or a file-level finding.
4. **Topic checks.** For each area the app uses, run the Verify list of its skill (`npx skills add ScaleDockHQ/PermDock --skill <name>`): `permdock-agents`, `permdock-approvals`, `permdock-tenancy`, `permdock-data`, `permdock-credentials`.
   ✓ Every item of every applicable Verify list has a pass or a finding.
5. **Tests.** No `describePolicy` suite, or one with `exhaustive: false`, is a finding: a new permission can ship untested. A custom `ApprovalStore`, `DecisionSink`, `MembershipSource`, `RoleSource`, `SnapshotSource`, `LimitStore`, `RelationSource` or `DirectoryStore` without its `test<Interface>` runner from `permdock/testing` is a finding.
   ✓ Every policy and custom store has its runner, or a finding.
6. **ASI02 and ASI03.** Map the inventory onto [OWASP Agentic](https://permdock.dev/docs/security/owasp-agentic); for the threat list itself, defer to the `owasp-agentic` spec skill (`npx skills add ScaleDockHQ/scaledock-skills --skill owasp-agentic`).
   - **ASI02** (tool misuse): unmapped tools, a collection permission on a row handler, a destructive tool without `approval`, capability lists that include denied tools.
   - **ASI03** (identity and privilege abuse): a model-supplied subject or actor, an actor used as approver, `distinct: false` on a sensitive action, a resume token not bound to permission, resource, subject and actor, API keys stored in plain text or created outside `decideCredential`, keys without expiry (PD029), and a `memberships` source applied to service-key subjects.
     ✓ Each agent adapter in the app has an ASI02 line and an ASI03 line.
7. **Pull request review**, when the scope is one PR. Review only what the diff changes:
   - Run `permdock collect --check` and `permdock usage --json` on both sides and compare. New leaves with no grant, grants for leaves nobody checks, and new `undeclared` or `outsideInclude` findings are comments.
   - A new or widened `allow` (a role gains a leaf, a `where` is dropped or loosened, a `to` becomes `anyone()` or `authenticated()`), a new policy `delegations` entry, or a removed `deny` needs a matching `describePolicy` row in the same PR.
   - A new model-reachable tool, or a new destructive action on an existing one, goes through the `permdock-agents` and `permdock-approvals` Verify lists.
   - A change to the `rls` config or generated RLS comes with `permdock rls generate --check` passing and an `rlsParity` or `rls verify` run.
   - `permdock doctor --json` on the head branch reports no new error.
     ✓ Every changed grant, leaf and tool has a comment on the changed line or an explicit pass.

## Verify before done

- [ ] The report leads with blockers: fail-open paths, a trusted model subject, a destructive tool without approval.
- [ ] Then ungranted and unused leaves, then closures that could be portable, then test gaps.
- [ ] Every finding names a file and a permission or role.
- [ ] The report ends with suggested PRs, one finding per PR when the fixes are independent.

## Reference index

- Topic Verify lists: the `permdock-agents`, `permdock-approvals`, `permdock-tenancy`, `permdock-data` and `permdock-credentials` skills.
- Docs: [OWASP Agentic mapping](https://permdock.dev/docs/security/owasp-agentic), [threat model](https://permdock.dev/docs/security/threat-model), [`permdock doctor`](https://permdock.dev/docs/cli/doctor), [`permdock usage`](https://permdock.dev/docs/cli/usage), [testing](https://permdock.dev/docs/adapters/testing).
