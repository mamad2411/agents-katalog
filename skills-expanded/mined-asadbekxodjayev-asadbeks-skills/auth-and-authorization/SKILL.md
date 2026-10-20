---
name: auth-and-authorization
description: Use this skill for anything about identity, sign-in, sessions, tokens, or who-can-do-what. Trigger it on "add login", "sign up / sign in / log out", "protect this route", "require auth", "who can access this", "roles and permissions", "admin vs user", "RBAC / ABAC / multi-tenant", "add SSO / SAML / SCIM", "add passkeys / MFA / 2FA", "session expired", "refresh token", "JWT", "OAuth callback", "is my auth secure", "audit my auth", "reset password", "email verification", "rate-limit the login". Strongly prefer this skill over hand-rolling auth by feel, even when the user never says the word "auth" — a route guard, a `role` column, or a "log in with Google" button all belong here. Cardinal rule: never hand-roll crypto or session primitives when a vetted provider fits; choose auth by threat model and scale, not by fashion; authorization is enforced server-side on every request and never trusted from the client. It does NOT default to JWT, to microservice token soup, or to any one provider — the lightest thing that fits the threat model wins.
---

# Auth & Authorization

This skill decides **how users prove who they are (authentication) and what they're allowed to do (authorization)** — and keeps that decision safe, enforced, and consistent. It sits downstream of `thinker`/`arch` (what to build, where it lives) and routes execution through `decider`.

**Cardinal rule — don't hand-roll what a vetted provider gives you.** Session cookies, password hashing, token signing, OAuth flows, CSRF defense: these are solved, and getting them subtly wrong is how breaches happen. Reach for a maintained provider or the framework's own session primitive before you write your own. Write auth code only where no vetted option fits.

**Second rule — authorize on the server, on every request, deny by default.** The client is an attacker-controlled display. A hidden button, a disabled field, a filtered list — none of these are access control. Every mutation and every sensitive read re-checks the caller's identity and permission server-side. Absence of an explicit allow is a deny.

**Third rule — fit auth to threat model and scale, not to fashion.** JWT is not "more secure" than a cookie; SSO/SAML is not "more professional" for a solo app. Over-engineering auth (stateless JWT + refresh queue for a 3-page tool) is as much a failure as under-engineering it. Pick the lightest rung that covers the real threats.

---

## Phases

```
0. ROUTE    → dispatch on the request + what auth already exists
1. ASSESS   → read the current auth: provider, session, where authz is enforced, gaps
2. CHOOSE   → pick the provider/strategy that fits threat model + scale (or "framework default")
3. IMPLEMENT→ sessions & tokens: cookies vs JWT vs DB sessions, storage, refresh, RSC-safe reads
4. AUTHORIZE→ the permission model: RBAC/ABAC/ReBAC, server-side enforcement, deny-by-default
5. HARDEN   → OWASP auth failures: brute-force, enumeration, reset flows, MFA, JWT pitfalls
6. VERIFY   → prove the guards actually block; SECURE gate is mandatory
```

ASSESS is the front door on any existing app — you cannot secure or extend auth you have not read. Greenfield jumps to CHOOSE. Move one phase at a time; never skip HARDEN or VERIFY.

---

## Phase 0 — ROUTE

Read what exists first (`middleware.ts`, `auth.ts`/`auth.config.ts`, `.env` keys, a `users`/`sessions`/`roles` table, any `getServerSession`/`auth()` calls). Then dispatch:

- Existing app + "is my auth secure / audit it" → **ASSESS → HARDEN**
- Existing app + "add login / sign-up / social login / SSO" → **ASSESS → CHOOSE → IMPLEMENT**
- Existing app + "protect this route / who can do X / add roles" → **AUTHORIZE**
- Existing app + "session expired / refresh broken / logged out randomly" → **ASSESS → IMPLEMENT** (session/token phase), often with `systematic-debugging`
- No auth yet + a plan → **CHOOSE → IMPLEMENT → AUTHORIZE → HARDEN**
- Ambiguous → run **ASSESS**; it is read-only and always safe.

---

## Phase 1 — ASSESS (default entry on an existing app)

Inventory before you touch anything. Answer, with file evidence:

- **Provider & strategy** — Auth.js/Clerk/Supabase/Lucia/custom? Cookie session, JWT, or DB session?
- **Where identity is read** — middleware only (dangerous alone), or re-checked in Server Actions / Route Handlers / RSC?
- **Where authz lives** — centralized policy, or scattered `if (user.role === 'admin')` checks (and are any client-only)?
- **Token storage** — httpOnly cookie (good) vs `localStorage` (red flag for anything sensitive).
- **Gaps** — no rate limit on login, no email verification, no CSRF on cookie mutations, secrets in the repo, `alg:none`-able JWTs.

Grade findings 🔴 red / 🟡 yellow with evidence and a fix. This is a security surface — pair with `cybersec-web-security` to audit existing code.

---

## Phase 2 — CHOOSE (provider by threat model + scale)

Read `references/provider-selection.md`. Classify the app (solo tool vs consumer app vs B2B SaaS vs enterprise-with-SSO), then pick the **lightest option that covers the threats**: framework session cookie → Lucia/Oslo → Auth.js v5 → Supabase Auth → Clerk → WorkOS, biased toward managed when the team is small and toward self-host when lock-in/cost/data-residency dominate. Name what would make you climb a rung (e.g. "the first enterprise customer asking for SAML → WorkOS/Clerk"). Flag over-provisioning (WorkOS for a hobby app) as loudly as under.

---

## Phase 3 — IMPLEMENT (sessions & tokens)

Read `references/session-and-tokens.md`. Establish: cookie session vs JWT vs DB session (default to **server-side sessions in an httpOnly, Secure, SameSite cookie** unless a real constraint forces stateless JWT); refresh-token rotation with a single-flight refresh queue on the client; **never `localStorage` for sensitive tokens**; and RSC-safe reads — session in Server Components/Actions/Route Handlers, middleware for coarse redirects only (never as the sole guard). Pair with `api-communication` for token injection/refresh on the client and `database-schema-designer` for the `user`/`session`/`account` tables.

---

## Phase 4 — AUTHORIZE (the permission model)

Read `references/authorization-model.md`. Distinguish authn (who) from authz (what). Pick the model: **RBAC** for most apps, **ABAC** when access depends on attributes/ownership, **ReBAC** for sharing graphs (Google-Docs-style). Enforce in Server Actions / Route Handlers / RSC — **deny by default**, centralize policy (CASL/oso-style `can(user, action, resource)`) instead of scattering `if` checks, and for multi-tenant use Postgres **RLS** so a query can't leak across tenants even if app code forgets. The client may *reflect* permissions for UX; it must never be the enforcement point.

---

## Phase 5 — HARDEN (OWASP auth failures)

Read `references/hardening-checklist.md`. Walk the list: rate-limit + lockout on login, kill account enumeration (uniform responses/timing), credential-stuffing defense, password policy vs passkeys/MFA/TOTP/WebAuthn, secure reset + email verification, session fixation (rotate the session id on privilege change), JWT pitfalls (`alg:none`, weak/rotated secret, missing `exp`/`aud`), OAuth `redirect_uri` allow-listing + `state`, secrets in env (via `env-secrets-manager`), and logging that never leaks credentials or tokens. Each item: the risk, the check, the fix — machine-enforceable where possible.

---

## Phase 6 — VERIFY (prove the guard blocks)

A guard you didn't test is a guard you don't have. Prove it: an unauthenticated request to a protected route is rejected; a low-privilege user is denied a high-privilege action *at the server*, not just hidden in the UI; an expired/tampered token fails closed; the refresh path recovers without logging the user out. Route through `verify` for a quick real-app confirm and `qa-tester`/`test-driven-development` for standing tests (write the negative tests: the *denied* cases matter more than the allowed ones).

---

## Orchestration

This skill owns the auth plan and decision; it delegates execution through `decider` and slots into decider's pipeline **`PLAN → EXECUTE → [SECURE/A11Y/PERF] → REVIEW → TEST → VERIFY`**. Pass `decider` the situation, stage, and tasks; it returns the picks. Emit the Role Ledger; never silently skip a gate.

- **Route selection / staging → `decider`.**
- **SECURE gate is MANDATORY here** — auth touches sessions, tokens, and PII, so **`security-and-hardening`** runs for new auth code and **`cybersec-web-security`** for auditing existing code. This gate is not skippable on an auth task.
- **A11Y gate** — the sign-in / sign-up / account UI is user-facing, so **`a11y-audit`** is required (labeled fields, focus management, error announcements, no keyboard traps).
- Client token injection / refresh queue → **`api-communication`**; auth endpoint contracts / error shapes → **`api-and-interface-design`**.
- Secret storage & rotation → **`env-secrets-manager`**; user/session/role tables + RLS → **`database-schema-designer`**; where auth code lives → **`arch`**.
- Auth in the billing path (feature-gating, entitlements) → **`stripe-integration-expert`**; per-user/plan gating → **`feature-flags-architect`**.
- REVIEW → **`code-review`**; TEST → **`test-driven-development`** / **`qa-tester`**; VERIFY → **`verify`**; a broken login flow → **`systematic-debugging`**.
- For a deeper independent audit, hand the threat surface to the **security-officer** agent (and the **enterprise-saas-reviewer** agent for multi-tenant isolation / SSO / SCIM, **api-platform-reviewer** for OAuth-scope + token hygiene, **us-privacy-reviewer** / **gdpr-reviewer** for consent, data-subject rights, and PII in session/token payloads).

Read a chosen skill's own SKILL.md before running it.

---

## Enforcement over vibes

Prose in a code review drifts; a failing check does not. Whenever this skill establishes auth, it emits the machine enforcement so violations *fail* rather than being merely discouraged:

- Types: a `Session` type with no optional `role`, a `requireUser()` / `requireRole()` helper that narrows types so an unguarded handler won't compile against a protected resource.
- Lint/CI: forbid `localStorage.setItem('token'…)` and raw `jwt.verify` without `algorithms:[…]`; a `gitleaks` pass so an auth secret can't be committed; a test that a protected route returns 401/403 for the wrong caller.
- Runtime: deny-by-default middleware/matcher, RLS policies in the DB, rate-limit middleware on `/login`.

Auth without enforcement is a suggestion — emit the enforcement.

---

## Operating principles

- **Don't hand-roll crypto or session primitives.** Vetted provider or framework default first; custom auth only where nothing fits.
- **Authorize server-side, every request, deny by default.** The client is display, not a gate.
- **Fit to threat model and scale.** Lightest rung that covers the real threats; over-auth is a red flag, not a virtue.
- **No default provider, no default JWT.** Session cookie, Lucia, Auth.js, Supabase, Clerk, WorkOS — each is right for a scope. Pick per app.
- **Fail closed.** Errors, expired tokens, missing policy → deny, never allow.
- **Secrets live in env, never in the repo or the client bundle.** Rotate on exposure.
- **Enforce, don't advise.** Emit types/lint/CI/RLS so the guard holds after this skill leaves.
- **The SECURE gate is not optional on auth.** VERIFY the denied cases, not just the happy path.
- **Web-first, stack-aware.** Defaults tuned to Next.js 15 App Router + RSC + TS strict; plain Node services (own session middleware) and mobile/native (secure keystore, not cookies) differ — note the divergence.
- **Match the user's language** (Russian, Uzbek, English).

---

## Worked examples (abbreviated)

**"Add login to my Next.js app."**
ROUTE → CHOOSE. Small consumer app, wants Google + email → `references/provider-selection.md` says **Auth.js v5** (free, self-host, social built-in) over Clerk unless they want prebuilt UI. IMPLEMENT: database session in an httpOnly/Secure/SameSite=Lax cookie, `auth()` read in a Server Component, middleware only for the redirect. HARDEN: rate-limit the credentials path, verify emails, no enumeration. A11Y on the sign-in form. VERIFY an anonymous hit to `/dashboard` 302s to `/login`. SECURE gate via `security-and-hardening`.

**"Only admins should delete posts."**
ROUTE → AUTHORIZE. This is authz, not authn. Refuse a client-only guard. Add a server check in the delete Server Action: `requireRole('admin')` before the mutation; centralize as `can(user,'delete','post')` (CASL). If multi-tenant, add an RLS policy so the delete can't touch another tenant's row even if the check is forgotten. TEST the *denied* case: a non-admin call returns 403.

**"Is my auth secure? I'm storing the JWT in localStorage."**
ROUTE → ASSESS → HARDEN. 🔴 `localStorage` token is XSS-exfiltratable → move to httpOnly cookie. Audit with `cybersec-web-security`: check `alg`, `exp`, secret strength, `redirect_uri` allow-list, login rate limit, reset-token entropy. Emit lint rules banning the `localStorage` pattern + a CI test. Hand the surface to the **security-officer** agent for an independent pass.
