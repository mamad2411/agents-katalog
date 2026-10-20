---
name: fedcm-basics
description: >
  Implement and review Federated Credential Management (FedCM) for browser-mediated
  identity federation between Identity Providers (IdP) and Relying Parties (RP). Use
  when replacing third-party cookie login flows, adding navigator.credentials.get with
  identity providers, configuring IdP well-known and config endpoints, client metadata,
  consent UX, or auditing FedCM privacy/security properties on owned IdPs and RPs.
---

# FedCM Basics

## Scope And Authorization

- **In scope:** IdP and RP origins you own, staging FedCM integrations, authorized browser security reviews.
- **Out of scope:** phishing real users, abusing another party’s IdP endpoints, or covert tracking research without authorization.
- Test in controlled browsers/profiles; document UX consent implications.
- Redact account identifiers, session tokens, and client secrets from notes.
- Pair implementation work with `code-quality-standards`.

## When To Use

- Migrating “Sign in with …” away from third-party cookies toward **FedCM**.
- Standing up IdP endpoints: `/.well-known/web-identity`, config URL, accounts endpoint, client metadata, ID assertion endpoint.
- RP integration with `navigator.credentials.get({ identity: { providers: [...] } })`.
- Reviewing disconnect, login status API, and mediation options (`optional`, `required`, `silent`).
- Threat-modeling IdP→RP token issuance under browser mediation.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Classic OAuth/OIDC token attacks | `api-auth-and-jwt-abuse` |
| SAML SSO assessment | `saml-sso-basics` |
| Account takeover chaining | `account-takeover-methodology` |
| Session fixation | `session-fixation-management` |
| Fetch Metadata CSRF isolation | `fetch-metadata-isolation` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Parties | IdP (accounts + tokens), RP (consumes identity), browser (mediates UX and privacy) |
| Key APIs | `navigator.credentials.get`, Login Status API, Identity Credential |
| IdP static config | well-known web-identity → config JSON (accounts_endpoint, client_metadata_endpoint, id_assertion_endpoint, …) |
| Privacy | browser limits passive tracking; user sees account chooser; RP need not iframe IdP arbitrarily |
| Security checks | client_id binding, origin allowlists, CORS on IdP endpoints, CSRF on assertion |

## FedCM endpoint map (IdP)

| Endpoint / resource | Role |
| --- | --- |
| `/.well-known/web-identity` | Points to config file URL for the IdP origin |
| Config JSON | Declares accounts, client metadata, ID assertion, optionally branding/disconnect |
| Accounts endpoint | Returns signed-in accounts for the browser chooser (credentials included as designed) |
| Client metadata endpoint | Validates RP `client_id`, may return privacy policy / terms URLs |
| ID assertion endpoint | Issues token/assertion for selected account + RP after user consent |
| Login Status API | Helps browser know IdP signed-in state without third-party cookies |

## Workflow

### 1. Confirm scope and success criteria

1. Record IdP origin(s), RP origin(s), client_ids, supported browsers, and whether replacing cookies or running in parallel.
2. Success: user completes FedCM sign-in on RP; wrong `client_id` or disallowed RP origin fails; silent mediation does not leak accounts inappropriately.
3. Note legal/privacy review for account sharing UX.

### 2. Inventory current federation

1. List existing OAuth/OIDC/SAML social-login paths and cookie dependencies.
2. Check browser support matrix for FedCM features you need.
3. Inventory RP callback handling: how assertion becomes a session (exchange code vs verify JWT).

```bash
# Owned IdP: confirm well-known and config reachability
curl -sS "https://idp.example/.well-known/web-identity"
curl -sS "https://idp.example/fedcm/config.json"
```

### 3. Baseline privacy and security

1. Confirm IdP endpoints do not reflect arbitrary origins without checks.
2. Confirm client metadata rejects unknown `client_id`.
3. Document whether top-level login status is set correctly after password login on IdP.

### 4. Implement or harden FedCM

**IdP**

1. Serve `/.well-known/web-identity` with `provider_urls` including your config.
2. Config JSON registers HTTPS endpoints only; keep config cacheable carefully (short TTL if secrets ever appear—prefer no secrets in config).
3. Accounts endpoint: require IdP session cookies as designed; return only needed display fields; stable account `id`.
4. Client metadata: map `client_id` → RP origins/privacy URLs; reject unknown clients.
5. ID assertion: bind token to RP identity (`client_id`, origin/nonce as applicable); short-lived assertions; audit log.
6. Implement disconnect if you support RP-initiated unlink.

**RP**

```javascript
// RP: request federated credential (illustrative)
const cred = await navigator.credentials.get({
  identity: {
    providers: [{
      configURL: "https://idp.example/fedcm/config.json",
      clientId: "rp-client-123",
      nonce: crypto.randomUUID(), // bind to server session if used
    }],
    // mediation: "optional" | "required" | "silent"
  },
});
if (cred) {
  await fetch("/auth/fedcm/callback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ token: cred.token }),
  });
}
```

1. Verify assertion server-side (signature, audience, nonce, expiry)—never trust browser alone.
2. Issue first-party session cookie with Secure/HttpOnly/SameSite as appropriate.
3. Handle user abort and `NetworkError` / privacy errors without account enumeration leaks in UI messages.

### 5. Verify with evidence

```text
# Manual browser checklist (Chrome DevTools → Network / FedCM where available)
# 1. First visit RP → chooser shows expected IdP accounts only when signed into IdP
# 2. Unknown clientId → failure, no token
# 3. Expired IdP session → prompts or fails cleanly
# 4. Replay old assertion to RP callback → rejected
```

```bash
# Server-side unit/integration tests (owned)
# - reject assertion with wrong audience
# - reject reused nonce
# - reject alg=none / unsigned tokens if JWT
```

### 6. Observe and harden

1. Metrics: FedCM success/fail, assertion exchange errors, disconnect events.
2. Alert on spike of unknown `client_id` hits (probing).
3. Keep IdP CORS and cookie flags reviewed when FedCM adds new endpoints.

### 7. Hand off

1. Document IdP config URLs, client_id issuance process, and RP callback verification steps.
2. Link privacy policy / branding assets; schedule browser regression when Chrome FedCM flags change.
3. Apply `code-quality-standards` for RP/IdP code shipped.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Assertion handling | Server verifies signature/aud/nonce | Trust `cred.token` client-side only |
| client_id | Allowlisted RP metadata | Any string accepted |
| UX | Clear consent; mediation intentional | Silent login without user expectation |
| Tokens | Short-lived, RP-bound | Long-lived portable tokens in logs |
| Fallback | Documented OAuth fallback | Broken login with no recovery |
| Testing | Multi-browser matrix | Single Canary-only path |

## Output Checklist

- [ ] IdP/RP origins, client_ids, authorization recorded
- [ ] Well-known + config + accounts + client metadata + assertion endpoints documented
- [ ] RP `navigator.credentials.get` integration reviewed
- [ ] Server-side assertion verification (aud/nonce/exp/sig)
- [ ] Unknown client and wrong-origin denials evidenced
- [ ] Session cookie flags and CSRF posture after login reviewed
- [ ] Login Status / disconnect behavior documented if used
- [ ] Metrics and abuse monitoring considered
- [ ] `code-quality-standards` applied if code shipped

## Rules

- Owned IdP/RP only; no unauthorized federation against third parties.
- Browser mediation is not a substitute for server-side token validation.
- Minimize PII in accounts endpoint display fields.
- Prefer HTTPS everywhere; no mixed-content IdP config.
- Route pure OAuth/JWT crypto issues to `api-auth-and-jwt-abuse`; keep this skill on FedCM wiring and threats.
