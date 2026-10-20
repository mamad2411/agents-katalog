---
name: pericles-tenant-isolation
version: 2026.05.2
description: >
  The non-negotiable multi-tenancy rules for Pericles. Use this WHENEVER code
  touches customer data, sets or reads organization_id, resolves a Skill, reads
  logs, or crosses any tenant boundary. Encodes the five isolation guarantees, the
  real enforcement model (organization_id is a validated input bound by the auth
  layer via UserOrganization), root-org global access, registry namespace
  resolution, and the P0 incident response for any suspected leak.
doctrine_refs: [Security §2, §6, §8; §9]
depends_on: [pericles-doctrine]
last_reconciled: 2026-05-28
---

# Pericles Tenant Isolation (build skill)

Tenants are mutually distrustful. No tenant should ever observe another tenant's
data — or even their existence. A violation is a P0. These guarantees are the floor
beneath every other Pericles skill.

> **Existing rule:** `.claude/rules/11-security.md` and `CLAUDE.md`
> ("Multi-Tenancy Pattern") are authoritative; this skill complements them.

## When to use this skill

Any code path that reads/writes customer data, sets/reads `organization_id`,
resolves Skills, reads invocation logs, or aggregates across customers.

## How isolation actually works in this codebase

`organization_id` appears as a **required input field** on every tool
(`z.string().uuid()`) and on every Prisma model except global/system rows. It is
**validated inside `execute`** and every query is filtered by it. The anti-forgery
property — a user can only act on *their own* org — is enforced at the **auth /
invocation layer**: `backend/src/auth` + `backend/src/server` authenticate the user,
and the `UserOrganization` join (with `role` ∈ OWNER/ADMIN/MEMBER/GUEST and a status)
determines which orgs that user may act on. So "don't trust the input" does **not**
mean "omit organization_id from inputs"; it means the invocation layer must bind the
input to the authenticated session and reject mismatches.

## The five guarantees (all non-negotiable)

1. **No tenant sees another tenant's data, ever** — `organization_id` on every
   query/tool/log read (`pericles-data-model`).
2. **No tenant sees another tenant's existence** — Custom Skill IDs include the
   tenant slug; platform listings exclude other tenants' Skills.
3. **No tenant's invocation is triggerable by another** — the authenticated session
   (+ `UserOrganization`) binds the acting org; a request cannot act on an org the
   user has no membership in.
4. **No Custom Skill resolves outside its namespace + platform** — registry
   resolution `tenant/<active>` → `platform`; other tenants unreachable
   (`pericles-skill-registry`).
5. **No Org Memory leak via shared platform Skills** — platform Skills receive the
   org and scope all access; the MCP layer enforces scoping at the data boundary
   (`pericles-mcp-layer`).

## Root organization carve-out

The root org (`Organization.is_root = true`, `@pericles.cloud` domain) has **global
access** by design. Root may read **aggregated, anonymized** cross-tenant data —
never raw tenant data outside the §9 path. Treat root access as privileged and
audited; never widen it.

## Org hierarchy: parent rollup access

A customer may be a **parent holding company with branded subsidiaries** modeled as
**child `Organization`s** (`parent_organization_id`) — each subsidiary is its own
tenant with its own `organization_id` and data (`pericles-data-model`). Access is
hierarchy-aware: `checkOrganizationAccess` (`backend/src/auth/middleware.ts`) grants a
user access when they have a **direct active `UserOrganization` membership**, **root-org
global access**, OR an **active membership in any ancestor org** (parent rollup). Access
flows **ancestor → descendant ONLY**: a parent-org member reaches its subsidiaries, but a
child- or sibling-org member never reaches a parent or sibling (the ancestor walk is
bounded + cycle-guarded). This does **not** relax Guarantee 1 — every query is still
filtered by a single `organization_id`; a parent "group view" is the **union across child
`organization_id`s**, each row still tenant-scoped, never a wildcard read.

## Registry namespace resolution

`resolve(skillId)` := `tenant/<active>` first, else `platform`. A platform-visibility
manifest may NOT reference a tenant Skill; tenant-depends-on-platform is the
supported pattern.

## §9 — the only sanctioned cross-tenant data path

Aggregation for cross-customer learning is allowed ONLY through per-tenant signal
extraction with formal differential-privacy budgets; budget exhaustion **halts**
aggregation (never fail-open). No customer-identifying context leaves a tenant. No
other cross-tenant access — not debugging, not "anonymized" ad-hoc queries
(`pericles-org-memory`).

## RBAC mapping (for the Admin Portal)

`UserOrganization.role` today is OWNER / ADMIN / MEMBER / GUEST. The Admin Portal
PRD's three tiers map roughly: OWNER+ADMIN → **Admin**, MEMBER → **Operator**,
GUEST → **Viewer**. The tier↔role reconciliation is owned by `pericles-admin-portal-ui`
(W1); flag it there rather than inventing a parallel scheme.

## P0 incident response

Confirmed cross-tenant leak / Custom Skill sandbox escape / non-allowlisted egress /
post-promotion version tamper → pause the affected capability platform-wide,
investigate, notify affected customers within 4h, postmortem within 5 business days,
prevention plan within 30 days. P1 = strong anomaly without confirmation
(investigate within 24h).

## Verification

Every tenant-scoped query filters on `organization_id`; the invocation layer rejects
an `organization_id` the authenticated user has no `UserOrganization` membership for;
registry resolution cannot reach another tenant's namespace; root access is limited
to aggregated/anonymized reads; the only cross-tenant code path is the §9 pipeline.

## Existing standards (read alongside)

`CLAUDE.md` (Multi-Tenancy Pattern); `.claude/rules/11-security.md`,
`.claude/rules/05-database.md`; `.cursor/rules/100-security/101-security-coding-standards.mdc`.

## Open questions

- The session → permitted-org binding point is `checkOrganizationAccess`
  (`backend/src/auth/middleware.ts`); it is the canonical helper but is not yet adopted
  by every endpoint (some still inline a `UserOrganization` membership check). Track
  endpoint adoption so the hierarchy rule applies uniformly.
- Differential-privacy budget mechanism specifics (per-tenant epsilon) — define with
  the platform team (Ops Spec §8).

## Changelog

- 2026.05.2 — Documented hierarchy-aware access: `checkOrganizationAccess` grants
  ancestor → descendant (parent rollup), child/sibling never reach a parent or sibling;
  branded subsidiaries are child orgs (`pericles-data-model`). Cited the binding helper.
- 2026.05.1 — Reconciled: organization_id is a validated input bound by the auth
  layer via UserOrganization (not omitted from inputs); added root-org global access
  and the OWNER/ADMIN/MEMBER/GUEST → tier mapping.
- 2026.05.0 — Initial draft from Skills Security Spec v1.
