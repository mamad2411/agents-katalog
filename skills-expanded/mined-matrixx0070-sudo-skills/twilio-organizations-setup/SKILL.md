---
name: twilio-organizations-setup
version: 1.0.0
description: Stand up Twilio Organizations to centrally govern multiple Twilio accounts with org-level SSO, roles, and the Organizations Public API.
author: matrixx0070
tags: [twilio, organizations, sso, saml, governance, iam]
capabilities: []
---

## When to use

Use this when your company runs more than one Twilio account and you need one control plane over all of them — centralized SSO, org-wide user management, and consistent roles instead of per-account logins. Reach for it when finance wants a single billing owner across accounts, when security mandates SAML sign-in for every Twilio user, or when you are onboarding a team that must access several accounts without separate credentials each.

**Not for:** issuing API Keys or rotating Auth Tokens for programmatic access — that is `twilio-iam-auth-setup`. Not for isolating a single customer's traffic and usage inside one account — that is subaccounts, covered under `twilio-numbers-senders` and `twilio-sms-isv-setup`. Organizations sits *above* accounts; subaccounts sit *inside* one account.

## Method

1. Confirm you have the Owner role on the accounts you want to unify, and that your plan/edition supports Organizations. Decision point: if accounts belong to different owners, consolidate ownership first — an org can only manage accounts it owns.
2. In the Console, create the Organization from the account switcher / org management area. Record the returned **Organization SID** (prefix `OR`).
3. Link existing accounts (Account SID prefix `AC`) into the Organization. Decision point: an account can belong to only one Organization — un-link before re-homing.
4. Configure org-level SSO: register your IdP (Okta, Entra ID, etc.) via SAML 2.0, map the ACS URL and entityID, and set up SCIM if you want automated user provisioning/deprovisioning.
5. Define cross-account roles at the org level (Administrator, Developer, Support, Billing) and assign users. Decision point: grant the narrowest role that lets the person work; reserve Administrator for break-glass.
6. Enforce SSO so password login is disabled for org members. Verify one non-admin user can sign in through the IdP before locking the door.
7. Use the Organizations Public API (`preview-iam`) to script user and role assignments at scale rather than clicking each one.
8. Document the account hierarchy: Organization → owned accounts → (optional) subaccounts, and who holds Owner on each.

## Example

```bash
# Read the accounts owned by an Organization via the Organizations Public API.
# Auth uses an org-scoped OAuth token (client-credentials), not Account SID/Auth Token.
curl -s "https://preview-iam.twilio.com/v1/Organizations/${ORG_SID}/Accounts" \
  -H "Authorization: Bearer ${ORG_OAUTH_TOKEN}"

# List role assignments for a user within the Organization.
curl -s "https://preview-iam.twilio.com/v1/Organizations/${ORG_SID}/RoleAssignments?Identity=${USER_ID}" \
  -H "Authorization: Bearer ${ORG_OAUTH_TOKEN}"
```

## Pitfalls

- **Confusing Organizations with subaccounts.** Organizations federate *separate* accounts for identity/governance; subaccounts partition traffic *within* one account. Picking the wrong layer means rebuilding your hierarchy.
- **No break-glass path after enforcing SSO.** If the IdP goes down and every user is SSO-only, nobody can log in. Keep one owner with a documented recovery method before you enforce.
- **Over-broad roles.** Assigning Administrator org-wide defeats least privilege. Map each person to Developer/Support/Billing and audit quarterly.
- **Stale account linkage.** An account silently owned by the wrong org won't appear where you expect. Verify the Organization SID on every `AC` account after linking.
- **Assuming org OAuth == account credentials.** The Organizations API uses org-scoped OAuth tokens, not the account's Auth Token; the wrong credential returns 401.

## Output format

```
# Twilio Organization Setup
ORG_SID: OR********************************
SSO: <IdP name> | protocol=SAML2.0 | SCIM=<on/off> | enforced=<yes/no>
ACCOUNTS LINKED:
- AC******************************** (<label>) owner=<name>
ROLES:
- <user> -> <Administrator|Developer|Support|Billing>
BREAK-GLASS: owner=<name> recovery=<method>
HIERARCHY: Org -> accounts[<n>] -> subaccounts[<n>]
```

## Reference

- **Organization SID** prefix `OR`; **Account SID** prefix `AC`. An Organization owns multiple accounts; each account may contain subaccounts.
- **Organizations Public API** is served under the `preview-iam.twilio.com` domain and authenticates with org-scoped **OAuth 2.0** tokens (client-credentials), distinct from account-level Account SID + Auth Token.
- **SSO** at org level uses **SAML 2.0** (register IdP metadata, ACS URL, entityID); **SCIM 2.0** enables automated user provisioning/deprovisioning.
- Org-level **roles** (Administrator, Developer, Support, Billing) apply across all owned accounts — this is the value over per-account users.
- Subaccounts are a data/traffic isolation feature inside a single account and are billed to the parent account; they are not part of the Organization identity layer.
