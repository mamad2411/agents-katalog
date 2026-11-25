---
name: pericles-admin-portal-ui
version: 2026.05.0
description: >
  How to build the Admin Portal — users/RBAC, SSO, integrations, Organizational Memory
  management, agent training, and the audit-log viewer. Use this WHENEVER you build or
  change any admin surface. Encodes the existing auth/RBAC substrate (UserOrganization
  roles, Google OAuth, JWT), the role→tier reconciliation, the read-only audit viewer,
  and the rule that permission/sharing changes are deliberate, audited admin actions.
doctrine_refs: [§7; Security §2; Ops §6; Admin Portal PRD]
depends_on: [pericles-frontend-foundations, pericles-tenant-isolation, pericles-observability, pericles-deployment-shapes]
last_reconciled: 2026-05-28
---

# Pericles Admin Portal UI (build skill)

The Admin Portal is where a customer administers their tenant: people and permissions,
SSO, ERP/data integrations, Organizational Memory, agent training/config, and the audit
trail. **The auth/RBAC substrate already exists** — build on it.

## When to use this skill

Building/changing any admin surface: users/roles, SSO, integrations, Org Memory mgmt,
agent training, audit viewer.

## Existing substrate (build on, don't reinvent)

- **Auth**: auth-server (`backend/src/server`, `auth`), JWT + `RefreshToken`, **Google
  OAuth** (`google-auth-library`). `components/auth` exists on the frontend.
- **RBAC**: `UserOrganization.role` ∈ OWNER / ADMIN / MEMBER / GUEST (+ status), unique
  `[user_id, organization_id]`, with invitation tracking. Org hierarchy via
  `parent_organization_id`; `is_root` for the platform root.
- **Audit**: `AuthAuditLog`, `MonitoringAuditLog` (`pericles-observability`).

## Role ↔ tier reconciliation (do this explicitly)

The Admin Portal PRD describes three tiers; the schema has four roles. Map:
OWNER+ADMIN → **Admin**, MEMBER → **Operator**, GUEST → **Viewer**. Implement one
mapping in one place and reuse it (don't invent a parallel scheme) —
`pericles-tenant-isolation` owns the canonical mapping.

## Surfaces

- **Users & RBAC** — invite/manage users, assign roles; changes are **deliberate,
  audited admin actions** (write to `AuthAuditLog`), gated to Admin tier. Never expose a
  way to silently widen access.
- **SSO** — configure Google OAuth (and enterprise SSO per shape); credentials handled
  server-side, never surfaced.
- **Integrations** — connect ERP (`pericles-erp-adapter`) and other sources via MCP
  (`pericles-mcp-layer`); show connection status; the ~30-min ERP connect that
  pre-loads Atlas.
- **Organizational Memory** — manage uploaded context/documents, review
  injection-screening flags (`pericles-org-memory`).
- **Agent training/config** — per-org tool enablement (`DataSourceToolConfig`),
  monitored risk types, severity/notification preferences.
- **Audit log viewer** — read-only view of the tenant's logs with lineage trees and
  export (CSV/JSON/PDF; Enterprise API). Scope and retention per deployment shape
  (`pericles-deployment-shapes`); **logs are never editable/deletable** from the UI
  (`pericles-observability`).

## What this forbids

Silent or un-audited permission changes; surfacing SSO/ERP credentials client-side;
editable/deletable audit logs; a parallel role scheme instead of the canonical
role→tier mapping; cross-tenant visibility (an admin sees only their tenant; root is the
only exception, aggregated/anonymized — `pericles-tenant-isolation`).

## Verification

RBAC uses `UserOrganization.role` with the canonical tier mapping; permission changes
write `AuthAuditLog` and are Admin-gated; SSO/ERP creds stay server-side; the audit
viewer is read-only with export; everything tenant-scoped.

## Existing standards (read alongside)

`.cursor/rules/001-application/003-pericles-admin-portal-core-standards-auto.mdc`;
`.cursor/rules/100-security/*`; Admin Portal PRD; `backend/src/{auth,server}`,
`frontend/src/components/auth`.

## Open questions

- Enterprise SSO providers beyond Google (SAML/OIDC) per shape — confirm with
  `pericles-deployment-shapes`.
- Whether agent-training config lives in `OrganizationSettings`/`DataSourceToolConfig`
  or a new store — confirm with `pericles-data-model`.

## Changelog

- 2026.05.0 — Initial draft; grounded in the existing auth/RBAC substrate
  (UserOrganization, Google OAuth, audit logs) and the role→tier reconciliation.
