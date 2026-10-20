---
name: integrate-oauth-oidc
description: Integrates a THIRD-PARTY identity provider via OpenID Connect — "Log in with Google/GitHub/Microsoft/Apple" or acting as an OAuth client to a third-party API. Uses the Authorization Code flow with PKCE (S256) everywhere (SPA, native, server); mandatory state (CSRF) + nonce (replay); exact-match redirect_uri; server-side code→token exchange (no client_secret in public clients); strict ID-token validation against JWKS; safe email_verified account linking; refresh rotation with reuse detection; system-browser-only native flows.
when_to_use: Adding "Sign in with <provider>", consuming a third-party OAuth API, validating an ID token, linking accounts across providers, or fixing a broken OAuth callback/redirect. Distinct from auth-jwt-session (that ISSUES and validates YOUR app's own session/JWT after this handshake completes — this skill is the third-party handshake itself) and design-authorization-model (what a user may DO — permissions — not who they ARE).
---

## When to Use

Reach for this skill when you are talking to an identity provider you do not own:

- "Add Log in with Google / GitHub / Microsoft / Apple"
- "Call the Stripe/Slack/Notion API on a user's behalf" (you are the OAuth client)
- "Validate this ID token / id_token / JWT from Google" — check signature + claims
- "A user signed up with Google but already has a password account — merge them"
- "My OAuth callback redirects but the token exchange / state check fails"
- "Refresh the access token / our Google refresh stopped working"
- "The native app login opens a webview and Google blocks it with disallowed_useragent"

NOT this skill:
- Issuing, signing, or verifying YOUR app's OWN session cookie / JWT AFTER login succeeds, refresh rotation of YOUR token, RP-initiated logout clearing YOUR session → **auth-jwt-session** (this skill ends when you have a validated set of claims; minting your session from them is that skill)
- "Which users can edit vs view", roles, multi-tenant isolation, per-resource rules → **design-authorization-model** (authZ — what they may do — not authN — who they are)
- Where to STORE the `client_secret` (Vault/Secrets Manager, OIDC-to-cloud, rotation, leak remediation) → **secrets-management**
- Auditing an existing diff for vulns by severity → **security-review**

## Steps

**1. Pick the flow — Authorization Code + PKCE, for every client type.**
- The implicit flow (`response_type=token`) is dead (deprecated by OAuth 2.1 / Security BCP) — never use it. So is ROPC (password grant). Use `response_type=code` always.
- PKCE (`code_challenge` + `code_verifier`) is mandatory for ALL clients now, including confidential server apps — not just SPA/native.

| Client | client_secret? | PKCE | Token exchange runs |
|---|---|---|---|
| Server / web app (BFF) | yes (server-only) | yes | server |
| SPA (React/Vue) | **no** | yes | **server (BFF)** — never the browser |
| Native / mobile | **no** | yes | server, or native via AppAuth |
| CLI | no | yes | local loopback or device code |

**2. Build the authorize request with state + nonce + PKCE.**
- `code_verifier` = 43–128 random chars; `code_challenge = BASE64URL(SHA256(verifier))`, send `code_challenge_method=S256` (never `plain`).
- `state` = random, server-stored, tied to the user's session → verify on callback. This is your **CSRF** defense; a missing/unchecked state lets an attacker inject their own auth code.
- `nonce` (OIDC) = random, stored, sent on authorize → **must equal** the `nonce` claim in the returned ID token. This is your **ID-token replay** defense.
- `redirect_uri` must **exactly** match a value pre-registered with the provider (scheme, host, port, path, trailing slash — byte-for-byte). No wildcards; "almost matches" = error or open redirect.

**3. Do the code→token exchange SERVER-SIDE. Never ship a secret to a public client.**
- POST `code` + `code_verifier` (+ `client_secret` only if confidential) to the token endpoint from your backend.
- A `client_secret` in SPA JS, mobile binary, or a public repo IS published — anyone can extract it. SPA/mobile use **PKCE without a secret** (it replaces the secret) behind a Backend-for-Frontend (BFF) that holds any secret and sets an httpOnly session cookie.
- Store the `client_secret` per **secrets-management** (env/Vault), never in source.

**4. VALIDATE the ID token — this is where most integrations are silently broken.**
- Fetch the provider's **JWKS** (`jwks_uri` from `/.well-known/openid-configuration`), select the key by the token's `kid`, **verify the signature**. Cache JWKS; refresh on unknown `kid`.
- **alg allowlist:** accept only what you expect (`["RS256"]` / `["ES256"]`). **Reject `alg:none`** and reject `HS256` when expecting RS — the RS→HS confusion attack signs with the public key as an HMAC secret. Never let the library read `alg` from the token.
- Check claims: `iss` == provider's exact issuer; `aud` == **your** `client_id` (reject tokens minted for another app); `exp` not past, `iat` not absurdly future (small clock skew ok); `nonce` == the one you sent.
- Only AFTER the token validates may you trust its claims or call `userinfo`. The `userinfo` response itself is not signed — trust comes from the validated ID token / the access token used to fetch it.

**5. Read verified claims, then hand off to YOUR app.**
- Standard OIDC claims: `sub` (the provider's STABLE user id — your join key, not email), `email`, `email_verified`, `name`, `picture`.
- Match users on `sub`, never on email alone (email is reassignable and provider-controlled). Now mint your own session/JWT — that is **auth-jwt-session**'s job; this skill is done at "validated claims".

**6. ACCOUNT LINKING — get this wrong and you enable account takeover.**
- Link an OAuth identity to an existing local account by email **only if `email_verified == true`** AND the provider is one you trust to verify email. If you auto-link on an unverified email, an attacker registers `victim@example.com` at a sloppy IdP and takes over the victim's account.
- Safer default: if an account with that email exists, require the user to **log in with the existing method first**, THEN link (first-party confirmation), instead of silently merging.
- Model identities as a separate table: one user → many `(provider, sub)` rows. A user with Google + GitHub + password is normal. Unique-constrain `(provider, sub)`.

**7. Refresh tokens — rotation, reuse detection, secure storage.**
- Request `offline_access` / `access_type=offline` only if you actually need long-lived access. Google returns a refresh token **only on the first consent** (or with `prompt=consent`) — capture and store it then.
- Rotate: each refresh use issues a new refresh token and invalidates the old. If an already-used (rotated) refresh token reappears → it was stolen → revoke the whole token family. (Mechanics overlap **auth-jwt-session**.)
- Storage: server-side or httpOnly `Secure` cookie; native → **Keychain (iOS) / Keystore (Android)**. **Never `localStorage`** (XSS reads it).

**8. Logout.**
- RP-initiated logout: redirect to the provider's `end_session_endpoint` with `id_token_hint` + `post_logout_redirect_uri` to end the provider session, and **revoke** the refresh token at the provider's revocation endpoint.
- Clearing YOUR app's own session/cookie is **auth-jwt-session**. Logging out of your app does NOT log the user out of Google unless you hit `end_session`.

**9. Scopes & incremental consent.**
- Request the **minimum** scopes at login (`openid profile email`). Ask for sensitive/extra scopes later, at the moment you need them (incremental consent) — broad upfront scopes scare users and over-privilege your token.

**10. NATIVE / mobile — system browser only, never a webview.**
- Use **ASWebAuthenticationSession** (iOS) / **Custom Tabs** (Android) via **AppAuth**. These share the system cookie jar (SSO) and isolate credentials from your app.
- **Never an embedded `WKWebView`/`WebView`**: Google (and others) block it (`disallowed_useragent`), it defeats SSO, and an embedded webview CAN read the user's IdP credentials — that is the whole point of avoiding it.
- PKCE is mandatory; redirect via a custom scheme or App Link/Universal Link that exact-matches registration.

**11. Apple Sign In quirks (and other provider gotchas).**
- Apple returns the user's **name only on the FIRST authorization** — persist it then or it's gone forever. Email may be a **private relay** (`@privaterelay.appleid.com`) the user can disable later — handle bounces.
- Provider table:

| Provider | Watch out for |
|---|---|
| Apple | name first-auth only; relay email; `client_secret` is a short-lived **JWT you sign** (ES256), not a static string — must regenerate |
| GitHub | OAuth, **not full OIDC** — no id_token; call `/user` + `/user/emails` with the access token; pick the `primary`+`verified` email |
| Microsoft (Entra) | `iss` varies per tenant; validate against `https://login.microsoftonline.com/{tid}/v2.0`; `v1.0` vs `v2.0` endpoints differ |
| Google | refresh token only on first consent / `prompt=consent`; `email_verified` reliable |

**12. Use a vetted library — do not hand-roll JWT validation or the flow.**

| Stack | Library |
|---|---|
| Node | `openid-client` |
| Python | `Authlib` |
| Java/Spring | Spring Security OAuth2 Client |
| Next.js / full-stack JS | NextAuth / Auth.js |
| iOS / Android | AppAuth |

These handle discovery, JWKS caching, PKCE, state/nonce, and clock skew correctly. Rolling your own ID-token verifier is the single most common source of `alg:none`/audience-confusion bugs.

## Common Errors

- **No PKCE / `code_challenge_method=plain`** — auth code interceptable. Always S256.
- **Skipping or not comparing `state`** — CSRF / code injection. Store server-side, compare on callback.
- **Trusting the ID token without checking `aud`** — a token minted for a DIFFERENT app of the same provider passes signature but is not for you. Require `aud == your client_id`.
- **`alg:none` / RS→HS confusion accepted** — verifier reads `alg` from the token. Hardcode an allowlist; reject `none` and unexpected algs.
- **`client_secret` shipped in SPA/mobile/repo** — it's public. PKCE replaces it; secret lives only server-side.
- **Auto-linking on unverified email** — account takeover. Link only when `email_verified` AND trusted IdP, or require existing-login confirmation.
- **Refresh token in `localStorage`** — XSS-readable. httpOnly cookie / Keychain.
- **Embedded webview for native login** — provider blocks it and it can steal IdP creds. System browser (ASWebAuthenticationSession / Custom Tabs).
- **redirect_uri "close enough"** — provider rejects, or a loose registration becomes an open redirect. Exact match, pre-registered.
- **Lost Apple name / dropped Google refresh token** — both arrive once. Persist on first response.

## Verify

1. Tamper one byte of the ID-token signature → validation rejects. Craft `alg:none` → rejected. Swap to `HS256` signed with the public key → rejected.
2. Token with wrong `aud` (another client_id) → rejected; expired `exp` → rejected; mismatched `nonce` → rejected.
3. Callback with a wrong/missing `state` → rejected. Token exchange with a wrong `code_verifier` → fails.
4. `grep` the SPA/mobile bundle for the `client_secret` → not present.
5. Account-link test: register `victim@x.com` at a provider that does NOT verify email → your app refuses to auto-link to the existing local account.
6. Refresh rotation: use a refresh token, replay the old one → family revoked, refresh fails.
7. Native: confirm login opens the system browser (ASWebAuthenticationSession / Custom Tabs), not an in-app webview.
8. Logout: after RP-initiated logout, the refresh token no longer mints access tokens at the provider.
