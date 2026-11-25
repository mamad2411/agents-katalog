---
name: workos-rbac-audit
description: Implement role-based access control with WorkOS roles and permissions, emit Audit Logs for sensitive actions, and store per-tenant secrets in Vault. Use for authorization and compliance work.
---

# WorkOS RBAC, Audit Logs, and Vault

## RBAC: roles and permissions

Model (configured in the WorkOS Dashboard under Roles):

- **Permissions** are fine-grained strings you define (`posts:delete`,
  `billing:manage`).
- **Roles** bundle permissions (`admin`, `member`, custom per-app roles) and
  are assigned per organization membership, so one user can be admin of org A
  and member of org B.
- Directory groups can auto-assign roles (group-to-role mapping per org).

Enforcement pattern:

```ts
// AuthKit session carries the claims:
const { user, role, permissions } = await withAuth();
if (!permissions?.includes("billing:manage")) return forbidden();
```

For APIs, the access token JWT includes role/permission claims; verify the
JWT (JWKS) and authorize on claims server-side. Rules:

- Check permissions, not role names, in code; roles change shape, permission
  strings are your stable contract.
- Deny by default; every sensitive handler starts with an explicit check.
- Re-fetch membership on privilege escalation paths instead of trusting a
  long-lived token minted before a role change.

Management via SDK: organization membership APIs
(`workos.userManagement.updateOrganizationMembership(...)` with a `roleSlug`)
let you build your own member management UI.

## Audit Logs

Emit an event for every action a customer security team would ask about
(logins are captured by WorkOS; you emit domain actions):

```ts
await workos.auditLogs.createEvent("org_123", {
  action: "document.deleted",
  occurredAt: new Date(),
  actor: { type: "user", id: user.id, name: user.email },
  targets: [{ type: "document", id: doc.id }],
  context: { location: req.ip, userAgent: req.headers["user-agent"] },
  metadata: { reason },
});
```

Practices:

- Define the action taxonomy in the Dashboard (schemas validate events).
- Emit from the server after the action commits, in the same request path;
  fire-and-forget with a retry queue so audit gaps do not fail user actions
  silently.
- Give enterprise customers self-serve access: Admin Portal `intent:
  "audit_logs"` for viewing/export, and Log Streams to push events into their
  SIEM (Datadog, Splunk, S3).
- Never put secrets or full PII payloads in metadata; log identifiers.

## Vault: per-tenant secrets

WorkOS Vault stores encrypted key-value secrets scoped to organizations,
useful for customer-supplied credentials (their API keys, tokens) with
per-tenant encryption keys:

```ts
const obj = await workos.vault.createObject({
  name: "acme-github-token",
  value: token,
  context: { organizationId: "org_123" },
});
const secret = await workos.vault.readObject({ id: obj.id });  // decrypts server-side
```

Rules: read at time of use, never cache decrypted values, and delete on
customer offboarding. Vault beats a `secrets` column because access is
audited and encryption is managed per context.

## Compliance quick wins

- Map each permission check to an audit event so authorization and evidence
  stay in sync.
- Retention and export requirements (SOC 2, ISO 27001) are satisfied by Log
  Streams plus Dashboard export; document where each lives.
