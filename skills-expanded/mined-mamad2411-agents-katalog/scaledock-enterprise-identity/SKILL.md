---
name: scaledock-enterprise-identity
description: Make a ScaleDock product enterprise-ready with SCIM 2.0 provisioning, OpenID Connect and SAML 2.0 SSO, WebAuthn passkeys, Shared Signals (SSF, CAEP, RISC) session revocation, NIST SP 800-63-4 assurance levels, CIBA, FAPI 2.0 when needed, and SPIFFE or WIMSE workload identity, with PermDock turning directory groups and roles into permissions. Use when a customer asks for SSO, SAML, SCIM, passkeys, phishing-resistant MFA, an IAL, AAL or FAL target, automatic deprovisioning, continuous access evaluation, IdP-driven logout, approval on a separate device, Okta or Entra integration, high-security API profiles, or service-to-service identity.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.2.0"
---

# ScaleDock enterprise identity

Enterprise customers expect their identity provider to sign users in, provision and deprovision them, and revoke access the moment something changes. This skill wires those standards into a ScaleDock product and lets PermDock turn what the IdP says into permissions. The spec skills carry the rules of each standard.

**Follow the workflow below step by step.** Only add the parts the customer needs; each step names the input that switches it on.

## Inputs (fill in, or ask before starting)

- SSO: yes or no, the customer's IdP (Okta, Entra ID, Google Workspace, Keycloak, other), and the protocol (OIDC or SAML).
- Sign-in: passkeys (WebAuthn) yes or no; an assurance target (NIST SP 800-63-4 IAL, AAL and FAL) yes or no.
- Provisioning: SCIM yes or no.
- Revocation: Shared Signals (CAEP) yes or no; Back-Channel Logout yes or no.
- Decoupled approval: CIBA yes or no (the user confirms on a separate device, for example a call-center or agent-initiated action).
- Security profile: FAPI 2.0 yes or no (regulated finance, open banking, high-value APIs).
- Workloads: SPIFFE yes or no (service-to-service calls across trust domains); WIMSE yes or no (workload tokens and proofs on each HTTP call).
- Tenancy: the scope a directory maps onto (usually the organization).

## Skills to install

```bash
npx skills add ScaleDockHQ/scaledock-skills --skill openid-connect --skill saml --skill webauthn --skill scim --skill shared-signals --skill fedcm --skill credential-management --skill dbsc --skill fido-ctap --skill digital-credentials
npx skills add ScaleDockHQ/scaledock-skills --skill nist-800-63 --skill ciba --skill fapi --skill spiffe --skill wimse   # only when selected
npx skills add ScaleDockHQ/PermDock
```

`openid` (the umbrella over every OpenID Foundation spec) helps when the customer names a profile this skill does not cover, such as iGov or HEART. `scaledock-repo-standard` (`references/auth.md`, `references/data-permissions.md`) owns Supabase Auth, tenancy and RLS.

## Invariants

1. **The spec skills win on protocol details.** ID token validation follows `openid-connect`; SAML responses and assertions follow `saml`; passkey ceremonies follow `webauthn`; assurance levels follow `nist-800-63`; backchannel authentication follows `ciba`; provisioning endpoints follow `scim`; event tokens follow `shared-signals`; profile rules follow `fapi`; SVID checks follow `spiffe`; workload tokens and proofs follow `wimse`.
2. **The IdP authenticates; PermDock authorizes.** Directory groups and role claims become memberships and roles, and PermDock decides from those. No handler branches on a raw group name.
3. **SCIM writes, it never decides.** The SCIM endpoint stores users and groups per tenant; PermDock reads them through a membership source and drops role names that are not assignable.
4. **Deprovisioning is immediate.** A SCIM deactivation, a CAEP `session-revoked` or a Back-Channel Logout invalidates snapshots, closes open streams and cancels pending approvals for that principal.
5. **Tenants are isolated.** Every SCIM token, SSO connection and SSF stream belongs to one tenant, and nothing from one tenant's IdP can change another tenant's memberships.
6. **Workloads are not users.** A verified SPIFFE ID, WIMSE workload identifier or CI token becomes a workload principal, never a user, and gets only the permissions granted to that workload.

## Workflow

1. **Set the inputs.** Agree with the user which of SSO, passkeys, an assurance target, SCIM, revocation, CIBA, FAPI, SPIFFE and WIMSE apply per tenant.
   ✓ Every selected part names its IdP and tenant mapping.
2. **SSO and sign-in.** Connect the IdP through Supabase Auth (SAML as `saml` describes, or OIDC) or, for a custom resource server, validate tokens as `openid-connect` and `jwt` describe and resolve the subject with `subjectFromJwt` from `permdock/jwt`.
   -> [`references/stack.md`](references/stack.md)
   Offer passkeys as `webauthn` describes, and with an assurance target pick the IAL, AAL and FAL from `nist-800-63` and check the sign-in methods and federation meet them.
   ✓ A user from the IdP signs in to the right tenant, a token or assertion from another issuer is rejected, and the selected AAL is enforced.
3. **Provisioning.** Mount `scimHandler` from `permdock/scim` per tenant, following `scim` for endpoints, filtering and PATCH, and pass `directoryMembershipSource(store)` as `memberships`.
   ✓ Creating, updating and deactivating a user in the IdP changes what that user can do on the next request.
4. **Revocation.** Mount the `permdock/ssf` receiver (push or poll) as `shared-signals` describes, and handle Back-Channel Logout as a second input. Pass `revocations` and `approvals` so streams close and approvals cancel.
   ✓ A `session-revoked` event ends that session's access without waiting for a cache to expire.
5. **Profiles and workloads.** With FAPI, apply `fapi` and use the PermDock JWT `profile: 'fapi2'` option and `permdock openapi emit --profile fapi2`. With CIBA, act as a client of the customer's CIBA-capable OpenID Provider as `ciba` describes, and treat the returned ID token as the human confirmation on a PermDock approval. With SPIFFE, verify SVIDs as `spiffe` describes; with WIMSE, verify the workload token and its proof as `wimse` describes. Map both to workload principals.
   ✓ The selected profile's checks pass.
6. **Test and audit.** Add scenario tests for join, role change, deactivation and revocation with `permdock/testing`, then run `audit-permissions` from `ScaleDockHQ/PermDock`.
   ✓ Tests pass and the audit has no blocker.

## Verify before done

- [ ] Every selected spec skill's Verify list passes.
- [ ] No handler reads a raw IdP group name; roles come from PermDock memberships.
- [ ] Deactivation and `session-revoked` take effect on the next request and close open streams.
- [ ] SCIM tokens, SSO connections (OIDC and SAML) and SSF streams are scoped to one tenant each.
- [ ] `permdock doctor` reports no error, and `pnpm verify` passes.

## Reference index

- **[`references/stack.md`](references/stack.md)**: each spec mapped to the ScaleDock stack and the PermDock adapter.
