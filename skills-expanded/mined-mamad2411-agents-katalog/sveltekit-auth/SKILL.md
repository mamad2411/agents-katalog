---
name: sveltekit-auth
description: Use when implementing authentication or session management in SvelteKit including cookie sessions, OAuth flows, JWT validation, route protection via hooks, and the sv add auth CLI add-on.
---

# SvelteKit Auth

## Specialization

Expert guidance for authentication and session management in SvelteKit. Covers cookie-based sessions, OAuth 2.0 / OpenID Connect integration, JWT validation, protecting routes and server endpoints via the `handle` hook, using `locals` as the authenticated identity carrier, the `sv add auth` CLI add-on, and common third-party auth library patterns (Auth.js / `@auth/sveltekit`, Lucia).

## Trigger Conditions

- Implementing login, logout, or session management in a SvelteKit application.
- Protecting a route or API endpoint so it requires authentication.
- Integrating a third-party OAuth provider (Google, GitHub, etc.) into a SvelteKit app.
- Validating a JWT from an upstream identity provider inside a SvelteKit server.
- Using the `sv add auth` CLI add-on to scaffold authentication.
- Diagnosing auth redirect loops, `locals` not being populated, or session cookies not persisting.

## Scope Boundaries

In scope:

- Cookie-based session patterns: `cookies.set`, `cookies.get`, `cookies.delete` in hooks and endpoints.
- `locals` as the canonical authenticated-identity carrier throughout the request lifecycle.
- `handle` hook for authentication middleware: populating `event.locals.user` before handlers run.
- Route protection: returning `redirect(303, '/login')` from server load functions when `locals.user` is absent.
- Endpoint protection: returning `error(401)` or `error(403)` from `+server.ts` handlers.
- OAuth 2.0 / OIDC callback pattern: receiving the authorization code, exchanging for tokens, setting a session cookie.
- JWT validation: verifying signature, expiry, and audience inside a hook or server endpoint.
- Auth.js (`@auth/sveltekit`) integration: setup, `SvelteKitAuth` handle, `auth()` helper, session access.
- Lucia auth library integration: session management, user creation, session validation middleware.
- `sv add auth` CLI add-on: scaffolding options and customization points.
- CSRF protection for login forms (SvelteKit's built-in `checkOrigin`).
- Refresh token rotation patterns for long-lived sessions.

Out of scope:

- Authorization (role-based access control, permission evaluation) — this skill covers authentication (identity) only.
- Identity provider administration (creating OAuth apps, configuring IdP settings).
- Password hashing implementation details (use a library such as `argon2` or `bcrypt`; this skill documents where to call it, not the algorithm).
- Multi-factor authentication device management.

## Inputs

- Authentication method (cookie session, OAuth, JWT, or library-managed).
- Protected resources (routes, API endpoints, or both).
- Session lifetime requirements and refresh strategy.
- Identity provider(s) if OAuth/OIDC.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Auth hook implementation | `handle` in `hooks.server.ts` populating `event.locals.user` |
| Route protection | Server load function guard redirecting unauthenticated users |
| Session management | Cookie creation, validation, and deletion with correct attributes |
| `App.Locals` type declaration | `user` (or equivalent) typed in `src/app.d.ts` |
| Auth quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Protect a single route using a cookie session | `handle` populates `locals.user`; server load redirects when absent |
| L2 Practical Delivery | Full login/logout flow with session cookie | Login action sets cookie; logout action deletes it; all protected routes guarded |
| L3 Specialist Hardening | OAuth integration or JWT validation | Callback endpoint exchanges code for token; JWT verified in hook; refresh handled |
| L4 Expert Standardisation | Production-grade auth with library integration and refresh rotation | Auth.js or Lucia integrated; token rotation documented; security checklist passes |

## Workflow

1. Declare the user type in `src/app.d.ts`: add a `user` property (or `null`) to the `App.Locals` interface.
2. In `hooks.server.ts`, implement a `handle` function that reads the session cookie, validates it (DB lookup or JWT verification), and sets `event.locals.user = user` (or `null`).
3. In any server load function for a protected route, check `event.locals.user`; if absent, `throw redirect(303, '/login')`.
4. In any `+server.ts` handler for a protected endpoint, check `event.locals.user`; if absent, `throw error(401)`.
5. Implement the login action in `+page.server.ts`: validate credentials, create a session, and set a cookie with `cookies.set(name, value, { httpOnly: true, sameSite: 'lax', secure: true, path: '/' })`.
6. Implement the logout action: call `cookies.delete(name, { path: '/' })` and `throw redirect(303, '/login')`.
7. For OAuth: implement a `GET` handler in `src/routes/auth/callback/+server.ts` that exchanges the authorization code for tokens, creates a session, and redirects to the originally requested URL.
8. For JWT: in the `handle` hook, extract the `Authorization` header or cookie value, verify the signature and claims (exp, iss, aud), and reject with `error(401)` on failure.
9. For Auth.js: wrap the `handle` export with `SvelteKitAuth({ providers: [...] })`; access the session with `auth()` in server load functions.
10. Run the auth quality checklist.

## Auth Quality Checklist

- [ ] `App.Locals` is typed with a `user` property; `locals.user` is never `any`.
- [ ] Session cookies are set with `httpOnly: true`, `sameSite: 'lax'`, and `secure: true`.
- [ ] Session tokens are opaque random values (not user IDs or email addresses) OR JWTs with verified signatures.
- [ ] JWT verification checks signature, `exp`, `iss`, and `aud` before trusting any claim.
- [ ] All protected server load functions check `locals.user` before accessing data.
- [ ] All protected `+server.ts` handlers check `locals.user` before executing actions.
- [ ] Logout deletes the session from both the cookie and the server-side session store.
- [ ] OAuth state parameter is validated on callback to prevent CSRF.
- [ ] Redirect targets after login are validated against an allow-list to prevent open redirect attacks.
- [ ] Passwords are hashed with a memory-hard algorithm (`argon2id` or `bcrypt`); plaintext is never stored.
- [ ] Refresh token rotation invalidates the previous token immediately after issuing a new one.
- [ ] `checkOrigin` is not disabled in `svelte.config.js`.

## Security Notes

- Never store session tokens in `localStorage`; use `httpOnly` cookies to prevent XSS theft.
- `sameSite: 'lax'` prevents most CSRF attacks on login actions; use `sameSite: 'strict'` for highly sensitive mutations.
- The `secure` cookie attribute must be `true` in production; allow `false` only in local development without TLS.
- Validate `state` parameter in all OAuth callbacks; a missing or mismatched state indicates a potential CSRF attack and must abort the flow.
- Never log session tokens, access tokens, or refresh tokens — redact before any structured logging.
- Use `crypto.randomBytes` or the Web Crypto API to generate session identifiers; do not use `Math.random()`.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| `App.Locals` typing | Workflow step 1 |
| Auth middleware hook | Workflow step 2 |
| Route protection | Workflow step 3 |
| Endpoint protection | Workflow step 4 |
| Login / session creation | Workflow step 5 |
| Logout | Workflow step 6 |
| OAuth callback | Workflow step 7 |
| JWT validation | Workflow step 8 |
| Auth.js integration | Workflow step 9 |
| Security hardening | Security Notes + checklist |
| Quality validation | Auth Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
