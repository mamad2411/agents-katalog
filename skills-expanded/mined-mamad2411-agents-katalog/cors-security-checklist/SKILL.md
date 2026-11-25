---
name: cors-security-checklist
description: >
  Org-ready CORS security checklist for owned browser APIs: Origin allowlists,
  credentials, null origin, preflight headers, Vary/caching, expose-headers,
  and regression tests. Use for design reviews, release gates, or periodic audits;
  hand deep exploits to specialized CORS skills.
---

# CORS Security Checklist

## Scope And Authorization

- **In scope:** First-party APIs, SPAs, BFF gateways, and edge configs you own or audit with permission.
- **Out of scope:** Checklist-driven scanning of unauthorized third parties.
- Mark each item Pass / Fail / N/A with evidence links.
- Redact secrets in attached curl output.
- Pair code fixes with `code-quality-standards`.

## When To Use

- Release gate for a new cross-origin SPA↔API design.
- Annual or quarterly hardening review.
- Post-incident audit after a CORS finding.
- Onboarding template for platform teams standardizing middleware.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Active misconfig hunting / triage | `cors-cross-origin-misconfiguration` |
| Credentialed browser PoC | `cors-credentialed-requests` |
| null Origin deep dive | `cors-null-origin-deny` |
| Max-Age operations / design | `cors-preflight-cache`, `cors-preflight-cache-design` |
| CSRF tokens | `csrf-cross-site-request-forgery` |
| Implementation quality baseline | `code-quality-standards` |

## Checklist

### A. Threat model and deployment

| # | Control | Pass criteria |
| --- | --- | --- |
| A1 | Cross-origin necessity | Documented why API is not same-site; or plan to collapse origins |
| A2 | Auth mode | Cookie vs bearer-in-JS documented; impact of CORS stated |
| A3 | Environments | Separate allowlists for dev/stage/prod (no prod trust of localhost) |
| A4 | Non-browser clients | Acknowledged CORS is not API authz |

### B. Origin allowlist

| # | Control | Pass criteria |
| --- | --- | --- |
| B1 | Explicit allowlist | Exact origin strings (scheme+host+port) |
| B2 | No reflection | Unlisted Origin → no ACAO (or hard fail) |
| B3 | No weak predicates | No unanchored regex / contains / endsWith without parse |
| B4 | No wildcard with creds | Never `ACAO: *` + `ACAC: true` |
| B5 | null denied | `Origin: null` not allowed on auth APIs |
| B6 | Vary | `Vary: Origin` when ACAO varies |

### C. Credentials and methods

| # | Control | Pass criteria |
| --- | --- | --- |
| C1 | ACAC minimized | `true` only if cookies/client certs required |
| C2 | Cookie flags | `Secure`, appropriate `SameSite`, `Path`, `__Host-` where fit |
| C3 | CSRF | State-changing cookie auth still has CSRF defense |
| C4 | Allow-Methods | Explicit list; no unnecessary methods |
| C5 | Allow-Headers | Explicit list; no ACRH echo |
| C6 | Expose-Headers | Minimal; no sensitive header names exposed |

### D. Preflight and cache

| # | Control | Pass criteria |
| --- | --- | --- |
| D1 | OPTIONS handling | 2xx with CORS headers where browsers require |
| D2 | Max-Age | Documented per env; low during policy change |
| D3 | CDN OPTIONS | Not cross-origin poisoned; Vary or bypass |
| D4 | GET cache | Authenticated bodies not public-cached with wrong ACAO |

### E. Engineering hygiene

| # | Control | Pass criteria |
| --- | --- | --- |
| E1 | Central middleware | One library/policy module; not per-handler copy-paste |
| E2 | Tests | Unit/integration: evil origin, good origin, null, credentials |
| E3 | Config as code | Allowlist in reviewed config; PR required |
| E4 | Logging | Origin denials safe to log; no cookie values |
| E5 | Docs | SPA `credentials` and required headers documented for clients |

## Workflow

### 1. Scope the audit

1. List base URLs, middleware repos, and edge (CloudFront/API Gateway) CORS settings — edge and origin both.
2. Pull prior findings and exceptions.

### 2. Execute checklist with evidence

```bash
API='https://api.example.local/v1/me'
GOOD='https://app.example.com'
BAD='https://evil.example'

curl -sSI -H "Origin: $BAD" "$API" | tee /tmp/cors-bad.txt | rg -i 'access-control|vary|HTTP/'
curl -sSI -H "Origin: $GOOD" "$API" | tee /tmp/cors-good.txt | rg -i 'access-control|vary|HTTP/'
curl -sSI -H 'Origin: null' "$API" | tee /tmp/cors-null.txt | rg -i 'access-control|HTTP/'
curl -sSI -X OPTIONS "$API" \
  -H "Origin: $GOOD" \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type,authorization' \
  | tee /tmp/cors-opt.txt | rg -i 'access-control|HTTP/'
```

### 3. Code and edge review

```bash
rg -n 'Access-Control-Allow-Origin|AllowAnyOrigin|WithOrigins|cors\(' --glob '!node_modules'
# Also review Terraform/CDN CORS blocks
```

### 4. Score and remediate

1. Fail any B/C items on authenticated APIs → prioritize.
2. Open tickets with owner; link specialized skills for deep fix.
3. Re-test after fix; attach before/after headers.

### 5. Sign off

1. Store checklist sheet (Pass/Fail/N/A + evidence paths).
2. Schedule next review; track temporary exceptions with expiry.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Audit | Evidence per row | Checkbox green without curl |
| Allowlist | Exact origins in config | `*` “temporary” in prod |
| Ownership | Platform middleware owners | Every team invents CORS |
| Edge+app | Both reviewed | Only app, forget API Gateway |
| CSRF | Still enforced | “We have CORS so skip CSRF” |

## Output Checklist

- [ ] Surfaces (app, API, edge) listed
- [ ] Sections A–E completed with Pass/Fail/N/A
- [ ] curl evidence for good/bad/null/OPTIONS
- [ ] Code/edge review notes attached
- [ ] Failures ticketed with owners
- [ ] Retest after remediations
- [ ] Exceptions with expiry
- [ ] Next review date
- [ ] Specialized skill handoffs as needed
- [ ] `code-quality-standards` on middleware changes

## Rules

- Checklist is a gate, not a substitute for threat-specific deep dives.
- CORS does not authenticate clients; never mark “secure” if API trusts Origin alone for authz.
- Authorized systems only.
- Keep this skill as the **audit/checklist primary** for CORS.
