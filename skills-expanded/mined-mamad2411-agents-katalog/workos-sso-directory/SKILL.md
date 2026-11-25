---
name: workos-sso-directory
description: Add enterprise SSO (SAML/OIDC) and Directory Sync (SCIM) to a product with WorkOS, including Admin Portal onboarding and webhook-driven user lifecycle. Use when a customer org needs SSO or provisioning.
---

# WorkOS SSO and Directory Sync

WorkOS normalizes every identity provider (Okta, Entra ID, Google, generic
SAML/OIDC) behind one API, and every directory (SCIM, Okta, Entra, Google
Workspace) behind another. You integrate once; each customer connects their
own IdP.

## Data model

- **Organization**: one per customer company; connections and directories
  attach to it.
- **Connection**: an SSO link (SAML/OIDC) for an organization.
- **Directory**: a provisioning link (SCIM etc.) for an organization; yields
  directory users and groups.

## SSO sign-in flow

With AuthKit, SSO is mostly configuration: create the org, add a domain or
connection, and AuthKit routes users with that email domain to their IdP
automatically. Manual flow with the Node SDK:

```ts
const url = workos.sso.getAuthorizationUrl({
  organization: "org_123",          // or connection: "conn_123"
  clientId: process.env.WORKOS_CLIENT_ID,
  redirectUri: "https://app.example.com/sso/callback",
  state,                            // anti-CSRF, verify on return
});
// callback:
const { profile } = await workos.sso.getProfileAndToken({ code, clientId });
// profile.id, profile.email, profile.organizationId, profile.rawAttributes
```

Security notes:

- Always send and verify `state`.
- Trust `profile.organizationId` for tenant assignment, never an email domain
  match alone (spoofable via attacker-controlled IdP claims).
- Just-in-time account creation: key users on `profile.id` + organization,
  not on email, so email changes at the IdP do not orphan accounts.

## Onboarding customers: Admin Portal

Do not walk customer IT through XML by hand. Generate a scoped setup link:

```ts
const { link } = await workos.portal.generateLink({
  organization: "org_123",
  intent: "sso",            // or "dsync", "audit_logs", "log_streams"
});
```

The customer admin configures their IdP in a guided flow; the connection
becomes active when they finish. Links expire; generate on demand from your
admin UI.

## Directory Sync (SCIM provisioning)

Read the directory:

```ts
const users = await workos.directorySync.listUsers({ directory: "dir_123" });
const groups = await workos.directorySync.listGroups({ directory: "dir_123" });
```

React to lifecycle via webhooks (see `workos-setup` for signature checks):

- `dsync.user.created` / `dsync.user.updated`: provision or update the user.
- `dsync.user.deleted` (and deactivation states): **revoke access and kill
  active sessions immediately**; deprovisioning speed is the security point
  of SCIM.
- `dsync.group.user_added` / `dsync.group.user_removed`: map groups to roles
  or entitlements in your RBAC layer.

Design rules:

- Treat WorkOS as the source of truth for org membership; reconcile with a
  periodic full `listUsers` sweep to heal missed webhooks.
- Handle users present in the directory but never signed in (pre-provisioned)
  and the reverse (JIT users later claimed by a directory).
- Group-to-role mapping should be explicit per organization; expose it in
  your admin UI rather than hardcoding group names.

## Testing

Dashboard test organizations plus IdP dev tenants (Okta developer, Entra
free tier) cover the matrix. Test: fresh SSO user, deprovision mid-session,
group change, and connection deactivation.
