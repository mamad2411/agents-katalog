---
name: better-auth
description: Use when touching authentication, organizations, members, invitations, roles, sessions, two-factor, single sign-on or SCIM provisioning in this repository. Covers which checks belong to better-auth and which belong to our policies, why a rule enforced on our side alone is one its own endpoints walk past, the `before`-hook pattern for plan gating, and the tables it owns and we must not write by hand.
---

# better-auth in this repository

better-auth owns identity. It owns the `user`, `session`, `account`, `member`,
`invitation`, `organizationRole`, `ssoProvider` and `scimProvider` tables, and it owns the
endpoints that write them. Everything below follows from that one fact.

## The rule that costs the most to learn

**A check on our side is one a request straight to better-auth's own endpoint walks past.**

The seat limit taught this. Ours would have been a `Policy` on an RPC handler; an
invitation created through `POST /api/auth/organization/invite-member` never reaches that
handler. It is `membershipLimit` inside the plugin now, asked per invitation so an upgrade
lands on the next invite rather than the next deploy.

So, before adding a rule, ask **who owns the endpoint**:

| The rule is about                             | Where it goes                                                          |
| --------------------------------------------- | ---------------------------------------------------------------------- |
| Something better-auth's endpoints do          | Its own option (`membershipLimit`, `requiredRole`, `canGenerateToken`) |
| Something only our procedures do              | `withPolicy(...)` in the handler                                       |
| A **plan** question better-auth cannot answer | A `before` hook in `auth/Options.ts`                                   |

That third row is the pattern to copy. `/sso/register` and `/scim/generate-token` are both
gated on an entitlement that lives in a table better-auth has never heard of, so both are
`before` hooks calling a function the host supplies — `ssoEntitled`, `scimEntitled` — and
both are resolved per request rather than captured at startup.

## `before` hooks run ahead of a plugin's own middleware

This bit a real check. The SCIM seat limit started as a `before` hook on `/scim/v2/Users`,
reading the organization out of the bearer token. It worked, and it answered a **forged**
token with "this organization has no seats left" instead of "unauthorized" — a fact about
a tenant handed to somebody who failed to authenticate.

If a check needs an authenticated caller, it does not belong in a route `before` hook. That
one moved into `databaseHooks.user.create.before`, where the plugin has already verified the
token and `authenticatedScimOrganization` can read what it resolved.

## Permissions are one model, and ours mirror better-auth's names deliberately

`identity/Permission.ts` is handed to better-auth's access-control builder _and_ used by our
`Policy`. The resource and action names are better-auth's — `member:create`,
`invitation:create`, `organization:delete` — so its endpoints and our screens ask the same
question. `contact`, `billing`, `sso`, `scim`, `webhook` and `file` are ours, unknown to it,
governed only by our policies.

Where a grant looks too loose, check whether the plugin already enforces it. `sso:manage`
and `scim:manage` are owner-**and**-admin because `hasOrgAdminRole` and the SCIM plugin's
`requiredRole` are, and a tighter rule on our side would be one its API walks past.
Tightening means changing both.

## Never write its tables by hand

`pnpm seed` creates users **through the API**, because better-auth hashes with scrypt and a
row inserted by hand has a password nobody can sign in with. The one exception is SCIM
provisioning, where there is no password to set — those accounts sign in through SSO.

`member`, `invitation`, `organizationRole`, `ssoProvider` and `scimProvider` carry **no
row-level security**, and `0011_sso.sql` explains why at length: better-auth writes them
outside any `withOrgScope` transaction, so a policy in the usual shape would refuse its
inserts, and one making room for a null `app.current_org` would permit every unscoped read
while still reporting `relrowsecurity` as true. That is the appearance of defence.

## Where to look

- `packages/modules/iam/src/auth/Options.ts` — every plugin, every option, every hook
- `packages/modules/iam/src/auth/Auth.ts` — the seam where Effect meets its promise chain
- `packages/modules/iam/test/Sso.test.ts`, `Scim.test.ts` — the harness for testing a hook
- `docs/sso.md`, `docs/scim.md` — the long version, including what has never been run
  against a real identity provider
