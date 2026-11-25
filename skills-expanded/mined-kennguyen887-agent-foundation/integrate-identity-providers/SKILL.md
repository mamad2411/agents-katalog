---
name: integrate-identity-providers
description: Use when adding third-party login or identity verification to a backend — social login (Sign in with Google / Apple / Facebook) and national digital identity / KYC (e.g. Singpass) via the OIDC relying-party flow (authorization code + PKCE + state/nonce → token exchange), validating the resulting token (.well-known → JWKS signature + iss/aud/exp, or introspection), centralizing many IdPs behind one identity broker (e.g. Keycloak), mapping an external identity to your user by (provider, subject), and treating verified attributes as KYC-grade. Framework-flexible. The frontend login UI is in secure-a-frontend-app.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Integrate identity providers

Adding external **login** (Google/Apple/Facebook) and **identity verification / KYC** (e.g. Singpass)
to a backend, the right way: as an **OIDC relying party** that delegates auth to the provider and
**verifies the result cryptographically**. Examples name real public providers; the flow is a standard
so it ports to any language. principle → **▸ Example** → **▸ Other stacks**. The *frontend* login UI +
session (NextAuth, route guards) is `secure-a-frontend-app`; exposing *your own* API to partners is
`integrate-external-services` §5. This skill is the backend/server + verification side.

## Core principle
**Never roll your own identity or trust a client-supplied identity blob.** Delegate authentication to
an OIDC provider, **verify the returned token's signature + claims** yourself, then map the external
identity to your own user. For a KYC provider (Singpass), the returned attributes are
**authoritative** — store them as verified, don't let the user edit them.

## 1. The relying-party flow (authorization code + PKCE)
- **Redirect the user to the provider's `authorize` endpoint** with `state` (CSRF) + `nonce` (replay) +
  **PKCE** `code_challenge`; keep `state`/`code_verifier` server-side (or in a signed cookie). On the
  **callback**, check `state`, then **exchange the `code`** at the `token` endpoint for an
  `id_token` + `access_token`. Confidential clients authenticate the exchange with a **client secret or
  a signed `client_assertion` JWT** (private-key JWT) — never expose the secret to the browser.
  ```
  GET /authorize?response_type=code&client_id=…&redirect_uri=…&scope=openid profile&state=…&nonce=…&code_challenge=…&code_challenge_method=S256
  → callback ?code=…&state=…   → POST /token { code, code_verifier, client_assertion }  → { id_token, access_token }
  ```
- **Then fetch verified attributes** (the `userinfo` endpoint, or a provider-specific person API) using
  the access token. The user never hands you their identity — the provider asserts it.
▸ *Other stacks:* any OIDC/OAuth2 client lib (AppAuth, MSAL, passport-openidconnect, `golang.org/x/oauth2`).
Principle: authorization-code + PKCE, validate `state`, exchange server-side, fetch attributes — never
implicit/client-asserted identity.

## 2. Validate the token (what every service does)
- **Discover, then verify.** Fetch the provider's `/.well-known/openid-configuration` once (cache it)
  to get `jwks_uri` + endpoints; **verify the `id_token`/JWT signature against the JWKS** and check
  `iss`, `aud`, `exp`, and `nonce`. For opaque access tokens, **introspect** at the provider instead.
  **Cache the JWKS** (refresh on unknown `kid`); never skip signature verification.
  ```ts
  const { jwks_uri, issuer } = await discover(idpBaseUrl);          // .well-known, cached
  const claims = await verifyJwt(idToken, { jwks: jwks_uri, issuer, audience: clientId });  // sig + iss + aud + exp
  ```
▸ *Other stacks:* the same — discovery doc → JWKS → verify signature + standard claims, or token
introspection for opaque tokens. (You already saw the validate side in
`integrate-external-services` §5.)

## 3. Centralize many IdPs behind one broker
- **Don't make every service implement Google + Apple + Singpass.** Front them with **one identity
  broker** (e.g. Keycloak) that brokers each upstream IdP and issues **your own uniform token**; your
  services then validate just that one issuer (§2). Adding an IdP becomes a broker config change, not a
  fleet-wide code change.
▸ *Other stacks:* Auth0/Cognito/Okta/Keycloak as an identity broker; an internal auth service that
normalizes providers. Principle: one issuer your services trust, many upstream IdPs behind it.

## 4. Map an external identity to your user
- **Link by a stable `(provider, subject)` pair, not by email alone** — emails change and can be reused;
  the provider's `sub` is stable. Store **which IdP verified the user**; on first login, provision the
  user (and link additional providers to the same account deliberately).
  ```ts
  const identity = { provider: 'singpass', sub: claims.sub };        // stable key
  let user = await users.findByIdentity(identity) ?? await users.provisionFrom(identity, claims);
  ```
▸ *Other stacks:* an `identities` table keyed by `(provider, subject)` linked to one user. Principle:
stable subject is the key; email is a (mutable) attribute.

## 5. Identity verification (KYC) vs login
- A **national digital identity** (Singpass) returns **verified attributes** (legal name, national id,
  DOB). Treat them as **authoritative**: store a `verified` flag + the source + a timestamp, **don't let
  the user edit verified fields**, and re-verify on the schedule your compliance requires. This is
  stronger than social login (which only proves "controls this Google account"). Distinguish the two in
  your model — a "logged in via Google" user is not "identity-verified".
▸ *Other stacks:* any eID / KYC provider returns asserted attributes; record provenance + verified-at,
gate sensitive actions on verification level.

## Security checklist
- `state` + `nonce` + **PKCE** on every flow; reject a callback whose `state` doesn't match.
- **Verify signature + `iss`/`aud`/`exp`** on every token; cache JWKS; introspect opaque tokens.
- Confidential-client **secret/private key in a vault**, never in the client or the repo.
- **Never log tokens or PII** (id numbers) — mask (see `write-service-code` §7). Short-lived access
  tokens + refresh handling; store only what you need.

## Vendor recipes (step-by-step)
Step-by-step guides for specific providers live in [`references/`](./references/) and load **on demand**.
- [`references/keycloak.md`](./references/keycloak.md) — Keycloak as token authority + identity broker: discovery, JWKS verify, client-credentials (latency-safe TTL), brokering Google/Apple/Singpass.
- [`references/singpass.md`](./references/singpass.md) — Singpass (NDI OIDC) relying-party: private-key-JWT client assertion, JWE-encrypted ID token (decrypt → verify), hosted JWKS, verified Myinfo (KYC) attributes.
- *(more per provider — social login, …)*

## Verification
- Login uses **authorization-code + PKCE**, validates `state`, exchanges server-side — no implicit flow.
- Every token is **signature-verified against JWKS** with `iss`/`aud`/`exp` (or introspected); JWKS cached.
- Many IdPs sit behind **one broker/issuer** your services validate.
- Users are linked by **`(provider, subject)`**, not email; the verifying IdP is recorded.
- KYC attributes are stored **verified + provenance + timestamp**, not user-editable; verification level
  is distinct from "logged in".

## Related
- `secure-a-frontend-app` — the frontend login UI, NextAuth, session, route guards (the client side of this).
- `integrate-external-services` §5 (token introspection / partner edge), §2 (resilient HTTP to the IdP).
- `write-cross-cutting-code` (the guard that reads the verified identity) · `design-an-error-model` ·
  `write-service-code` §7 (mask PII).
