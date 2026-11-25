---
name: account-takeover-methodology
description: >
  Multi-vector account takeover (ATO) methodology for authorized testing: password
  reset, session, IDOR, token/OAuth, MFA bypass chains, and impact proof. Use when
  assessing owned apps or scoped bug bounties for full account compromise paths —
  not for unauthorized access, credential stuffing crime, or phishing real users.
---

# Account Takeover Methodology

## Scope And Authorization

- **In scope:** applications and identity flows you own, labs/CTFs, or programs with **written scope** allowing ATO testing.
- **Out of scope:** real-user phishing, buying/selling credentials, attacking out-of-scope IdPs, or accessing accounts without permission.
- Prefer dedicated test accounts; never pivot into production customer data.
- Redact tokens, session cookies, reset links, and PII from reports.
- Stop at proof-of-impact per program rules (often “read email setting” not “wipe account”).

## When To Use

- Systematic ATO assessment across authn, session, recovery, and OAuth.
- Chaining medium findings into **account compromise**.
- Building a regression checklist after a prior ATO incident.
- Coordinating with product security on severity (P1 account takeover).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Password-reset Host/token poisoning only | `password-reset-poisoning` |
| Session fixation only | `session-fixation-management` |
| OAuth/OIDC deep dive | `oauth` / catalog OAuth skills; `api-auth-and-jwt-abuse` |
| SAML SSO issues | `saml-sso-basics` |
| Lockout policy design | `account-lockout-design` |
| IDOR-only object authz | `idor-broken-object-authorization` |
| Engagement planning | `recon-and-methodology` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus — ATO surface map

| Surface | Failure modes (examples) |
| --- | --- |
| Registration | Duplicate account link, mass assignment role |
| Login | User enum, weak password policy, missing MFA |
| Session | Fixation, absolute session never expires, cookie `Secure`/`HttpOnly`/`SameSite` gaps |
| Password reset | Token leak in referrer, host header injection, weak token, reuse, no invalidation |
| MFA | Backup code reuse, response manipulation, brute OTP without rate limit |
| OAuth/OIDC | `redirect_uri` manipulation, token theft XSS, account linking without verify |
| API tokens | Long-lived PAT leak, JWT `alg` confusion, missing `aud` |
| IDOR / BOLA | Change victim email, OAuth link, 2FA settings via object id |
| Support / impersonation | Overbroad “login as user” without audit |
| Secondary email / phone | Unverified channel steals recovery |

## Workflow

### 1. Scope, accounts, and success criteria

1. Record program rules, allowed domains, test accounts (attacker A, victim B), MFA availability.
2. Success: documented path where A obtains B’s session or durable credentials **without B’s password**, with evidence.
3. Define stop conditions (no data destruction, no mass messaging).

### 2. Map identity flows (recon)

```bash
# Inventory auth endpoints (authorized staging)
curl -sS -D- -o /dev/null 'https://app.example/login'
curl -sS -D- -o /dev/null 'https://app.example/forgot-password'
# Capture redirects to IdP
curl -sS -D- -o /dev/null 'https://app.example/oauth/login'
```

1. Diagram: register → verify → login → MFA → session → reset → OAuth link → logout.
2. Note cookie flags, token storage (localStorage vs cookie), CSRF defenses.
3. List settings endpoints that change email, password, phone, SSO links.

### 3. Test each vector (isolated then chained)

**A. Password reset**

| Check | Probe idea |
| --- | --- |
| Token entropy / predictability | Request multiple tokens; compare |
| Token one-time + expiry | Reuse token; use after TTL |
| Host/header poisoning | `Host`, `X-Forwarded-Host` on reset request (see `password-reset-poisoning`) |
| Link leakage | Open graph/referrer, server logs, email partner |
| Session after reset | Are old sessions revoked? |

**B. Session**

| Check | Probe idea |
| --- | --- |
| Fixation | Set pre-login cookie; see if post-login retains id |
| XSS → cookie theft | Only if XSS in scope; HttpOnly matters |
| Concurrent sessions | Password change / logout-all |
| CSRF on state-changing auth | Link OAuth, disable MFA, change email |

**C. OAuth / social login**

| Check | Probe idea |
| --- | --- |
| `redirect_uri` | Partial match, localhost, scheme tricks |
| Account linking | Link provider to victim without proving email |
| Code/`state` | Missing state; stolen code reuse |

**D. IDOR on account settings**

```bash
# Victim B id guessed/leaked; attacker A session
curl -sS 'https://app.example/api/users/B/email' -H "Cookie: session=A" \
  -X PUT -H 'Content-Type: application/json' \
  -d '{"email":"attacker@evil.example"}'
```

**E. MFA**

| Check | Probe idea |
| --- | --- |
| OTP rate limit | Space attempts; response codes |
| Backup codes | Reuse; download without reauth |
| Disable MFA | CSRF or IDOR without password |
| Remember-me device | Token theft / predictable device id |

### 4. Chain to impact

1. Prefer chains: e.g. reset poisoning → login as B → IDOR admin flag; or XSS → session → disable MFA.
2. Prove control: read B-only resource, change B recovery email (if allowed), show session cookie for B.
3. Severity: unauthenticated ATO > authenticated priv-esc to other users > self-DoS.

### 5. Evidence package

```text
1. Precondition (accounts, versions)
2. Step-by-step requests (redacted)
3. Response proving access to B
4. Business impact statement
5. Remediation suggestions + retest notes
```

### 6. Remediation themes (for owners)

| Area | Control |
| --- | --- |
| Reset | High-entropy single-use tokens; bind to user; strip untrusted hosts; invalidate sessions on reset |
| Session | Rotate on login/privilege change; HttpOnly+Secure+SameSite; logout-all |
| OAuth | Exact redirect allowlist; `state`; careful account linking |
| Authz | Server-side checks on every account mutation |
| MFA | Rate limit OTP; reauth for disable; audit |
| Detect | Alerts on email/password/MFA changes, new device, reset storms |

### 7. Hand off

1. File one finding per chain (or one parent with children) per program preference.
2. Map regressions to automated tests where stable.
3. Route deep-dives to specialized skills rather than bloating the report methodology.

## Priority Test Order (time-boxed)

1. Password reset + email change IDOR  
2. OAuth redirect / linking  
3. Session fixation + cookie flags  
4. MFA disable / OTP brute  
5. Long-lived API tokens / JWT flaws  
6. Support impersonation  

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Ethics | Test accounts only | Touching real customer accounts |
| Science | Minimal chain with proof | “ theoretically XSS could ATO” without path |
| Scope | In-program hosts | IdP vendor core out of scope |
| Reporting | Redacted tokens | Full reset URLs in public screenshots |
| Fix advice | Concrete control + retest | “Use security best practices” only |

## Output Checklist

- [ ] Written scope and test accounts recorded
- [ ] Identity flow map complete
- [ ] Reset, session, OAuth, MFA, IDOR vectors tested or N/A justified
- [ ] At least one end-to-end chain attempted where partials exist
- [ ] Impact evidence saved (redacted)
- [ ] Remediation mapped to owners
- [ ] Neighbor skills used for deep issues
- [ ] No customer data retained beyond policy

## Rules

- Authorized ATO testing only; no real-world account crime.
- Minimize harm; respect bounty safe-harbor and rate limits.
- Evidence over speculation; chains must be reproducible.
- Redact all secrets in artifacts.
- This skill orchestrates multi-vector ATO; detailed single-class exploits belong to child skills.
