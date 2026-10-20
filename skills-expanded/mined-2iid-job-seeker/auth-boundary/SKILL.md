---
name: auth-boundary
description: Own the seam your identity provider does not — server-side token verification, mapping the provider identity to your tenant and roles, idempotent first-login provisioning, an exact-match redirect allowlist after callback, session invalidation on revocation, and the email-change / merge / deletion cases. Never reimplement password storage, MFA, or token issuance. Use when wiring or changing login, signup, SSO, callbacks, sessions, or logout. Trigger words — auth, login, signup, SSO, OAuth, OIDC, callback, redirect, session, logout, JWT, claims, provisioning, account merge, revocation, impersonation.
---
# Auth boundary (the seam the provider does not own)

**Use when:** wiring or changing any login/signup/SSO flow, callback handler, session lifecycle, or the mapping
from a provider identity to your users and roles. **Owners:** security-engineer, backend-engineer.
**Scope:** the provider owns credential storage, password policy, MFA, its own edge defences, key rotation, and
token issuance — **do not rebuild any of it.** This playbook covers only the seam you own, where the findings are.

## Inputs
The provider and flow in use, the role/tenant model from `docs/security/security-model.md`, the exact set of
post-login destinations the product needs, and what "revoked" must mean inside your application.

## Procedure
1. **Verify the token on the server, every request** — signature against the provider's published keys, plus
   issuer, audience, expiry, and the nonce/state you issued. **The client never tells the server who it is:** no
   user id, role, tenant, or email from a header, body, query string, or local storage is ever trusted.
2. **Map provider identity → your tenant and roles** in your own data. The join key is the provider's immutable
   subject id, **never the email** — emails get changed, reused, and spoofed across providers. Roles live in your
   DB; a claim read from the verified token is re-checked against your record before it grants anything.
3. **Provision idempotently on first login.** Upsert on `(provider, subject_id)` behind a **unique constraint**,
   in one transaction. Two tabs, a double-clicked callback, or a retried request must produce **one** account —
   this is the classic double-account bug. A collision with an existing email is an explicit, verified link,
   never a silent takeover.
4. **Allowlist the post-callback redirect.** Resolve the destination against a **server-side allowlist of exact
   paths/origins**; anything else falls back to a default landing page — never redirect to a URL taken from the
   request, and reject protocol-relative, encoded, and nested-parameter forms too. Open redirect is the top
   finding at this seam: it turns your login page into a credible phishing launcher.
5. **Invalidate sessions in YOUR application** — provider revocation does not reach your app-side session. Keep a
   session epoch on the user record, bump it on logout-everywhere, role change, password reset, and back-channel
   logout; every request compares its token's epoch and fails closed, with a TTL short enough that revocation is
   measured in minutes.
6. **Handle the lifecycle explicitly.** *Email change*: re-verify, keep the subject id as the key, bump the epoch.
   *Merge*: user-confirmed, audited, one direction, never automatic on a matching email. *Deletion*: revoke
   sessions first, then apply the retention/tombstone rule so foreign keys and the trail survive.
   *Impersonation*: a separate flow, always audited.
7. **Audit and limit the boundary.** Every login, failed login, role change, revocation, merge, and impersonation
   is an audit row (`audit-log`); login, signup, reset, and callback are throttled (`rate-limit`).
8. **Test — executed, all three:** (a) a callback carrying a **foreign redirect target is refused** and lands on
   the default page; (b) a **second login for the same subject creates no second account** (row count unchanged);
   (c) a **revoked/epoch-bumped session cannot read** a protected resource. Plus a deny test that a
   client-supplied role or user id changes nothing.
9. **Verify:** run `scripts/verify.sh`, drive the real flows against the running app, and record with
   `scripts/verify.sh --observe "<expected>" "<observed>"` the redirect target you actually landed on, the user
   row count before/after the second login, and the status code the revoked session got.

## Guardrails
- ❌ Rolling your own password hashing, MFA, or token signing; ❌ trusting an unverified token or a client claim.
- ❌ Email as the identity key; ❌ redirect target read from the request; ❌ provisioning without a unique constraint.
- ❌ A long-lived app session with no revocation path; ❌ silent account merge on a matching email.
- Auth code is sensitive by definition: it lands in `vantry.yml` `sensitive_paths` and cannot merge without a
  committed `.vantry/reviews/<branch-slug>.security.json` with `verdict: pass`.

## Give these tests a mechanical footprint
The tests above are the whole value of this playbook, and nothing made them run again. A walk satisfied every
clause of the old Done-when with a sentence in `--observe` and **no redirect, session-epoch or revocation test
anywhere in the tree**. Prose in a receipt is not a regression guard.

Wire them in, both ways:
1. They live in `run.test`, so every verification executes them.
2. Promote the **revocation** test to `vantry.yml` `acceptance:` — it is the one whose regression is silent and
   catastrophic:

```yaml
acceptance:
  - "AC-n | REQ-nnn | a revoked session is refused on the next request | <the command that runs that ONE test>"
```

That line runs on every `scripts/verify.sh`, lands in the receipt naming the requirement, and blocks the push of
someone who breaks it in six months without ever having heard of it.

## Done when
- The server derives identity from the verified token/session **only**, never from a client-supplied id — proven
  by a test that sends a forged id and gets 401/403.
- A **revoked session is refused on the next request**, proven by an executed test that is promoted to
  `vantry.yml` `acceptance:` and appears in the receipt.
- Redirect targets are matched against an **exact allowlist**, proven by a test that sends an external URL.
- Identity is keyed on the **subject id**, not the email, with a unique constraint — proven by a test that
  changes an email and keeps the account.
- `scripts/verify.sh` passes and `--observe` quotes the observed status codes, not a summary of intent.
Tokens are verified server-side; identity maps to tenant/roles by subject id in your DB; provisioning is
unique-constrained and idempotent; the redirect allowlist is exact-match; revocation invalidates app sessions;
and a **fresh passing receipt** for this branch whose observation quotes the **refused foreign redirect**, the
**unchanged user count after a second login**, and the **status code of the revoked session**. Delegate tables to
`safe-migration`/`rls-policy`, the trail to `audit-log`, the throttle to `rate-limit`.

## Stack notes — Supabase Auth / Clerk / Auth0 on Next.js (illustration, not contract)
Verify in middleware or a server helper, never a client component; keep `users(provider, subject_id UNIQUE,
tenant_id, role, session_epoch)` in your own schema and join RLS to it; hold `ALLOWED_REDIRECTS` as a server
constant checked before any redirect; consume the provider's back-channel logout / user-updated event
(`webhook-handler`) to bump `session_epoch`. If `CLAUDE.md` names a different stack, this section is void and the
Procedure above still applies.
