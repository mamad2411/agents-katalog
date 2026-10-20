---
name: cors-preflight-cache-design
description: >
  Design Access-Control-Max-Age and preflight-related CORS headers for owned APIs:
  choose TTLs, minimize non-simple requests from SPAs, set stable Allow-Methods/Headers,
  and plan rollout so security changes are not trapped behind long browser preflight
  caches. Use when building or revising CORS middleware policy, not only incident response.
---

# CORS Preflight Cache Design

## Scope And Authorization

- **In scope:** Designing CORS preflight policy for APIs/SPAs you own.
- **Out of scope:** Using Max-Age tricks on systems outside authorization; claiming Max-Age alone fixes reflection bugs.
- Validate in staging browsers (Chrome, Safari, Firefox) before production TTL increases.
- Pair implementation with `code-quality-standards`; use `cors-preflight-cache` for production troubleshooting.

## When To Use

- Greenfield SPA/API split needing credentialed or header-rich CORS.
- Reducing OPTIONS load by design (not one-off firefighting).
- Setting org defaults for Max-Age by environment (dev vs prod).
- Coordinating CORS allowlist changes with safe TTL strategy.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Live OPTIONS storm / CDN OPTIONS bug | `cors-preflight-cache` |
| Origin allowlist security review | `cors-cross-origin-misconfiguration` |
| Credentialed CORS rules | `cors-credentialed-requests` |
| Org checklist audit | `cors-security-checklist` |
| Implementation quality baseline | `code-quality-standards` |

## Design goals

| Goal | Lever |
| --- | --- |
| Fewer preflights | Lower custom headers; prefer simple requests where safe; longer Max-Age when stable |
| Fast security rollback | Shorter Max-Age; feature-flag allow headers |
| Correctness | Explicit Allow-Methods/Headers; no reflection of ACRH |
| Cache safety at edge | Do not share OPTIONS across Origins; Vary correctly |

## Workflow

### 1. Map which calls need preflight

Non-simple examples:

- Methods: `PUT`, `PATCH`, `DELETE`, … 
- Headers: `Authorization`, `X-Request-Id`, non-simple `Content-Type` (`application/json`)
- Advanced: readable response headers needing `Expose-Headers`

```text
Inventory table:
| Client call | Method | Headers | Preflight? | Auth |
```

### 2. Minimize avoidable preflights (product/API design)

1. Prefer `Authorization` patterns that still need preflight for JSON APIs — accept OPTIONS cost rather than weakening auth.
2. Avoid inventing many custom headers; use one `X-Correlation-Id` if needed.
3. Same-site deployments (`app` and `api` under one eTLD+1 with reverse proxy) can eliminate cross-origin needs entirely — best performance design.
4. For public read-only GETs without custom headers, simple requests may skip preflight — still set ACAO correctly.

### 3. Choose Max-Age by environment

| Environment | Suggested starting Max-Age | Rationale |
| --- | --- | --- |
| Local/dev | 0–60 | Policy changes constantly |
| Staging | 60–600 | Test realism without long sticky mistakes |
| Production (stable policy) | 600–7200 | Balance OPTIONS reduction vs change lag |
| Production during CORS incident | 0–60 | Force revalidation |

Document browser maximums as soft caps; do not rely on values above known engine limits.

### 4. Specify stable preflight response shape

```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type, X-Request-Id
Access-Control-Max-Age: 3600
Vary: Origin, Access-Control-Request-Method, Access-Control-Request-Headers
```

Rules:

1. Allow-Headers is an **explicit list**, not a mirror of attacker-supplied ACRH.
2. Allow-Methods is explicit; avoid `*` with credentials.
3. ACAO from allowlist only (see credentialed skill).
4. Include `OPTIONS` in route handling; do not 401 OPTIONS before CORS headers if browsers need 2xx preflight (framework-dependent — test).

### 5. Rollout plan for policy changes

1. Ship **expanded** allow lists first (superset), wait one old Max-Age period, then remove deprecated headers/methods.
2. When **removing** capabilities: lower Max-Age in advance, deploy, wait, then raise Max-Age.
3. Version SPA and API deploys so old SPAs are not stuck calling removed headers.

### 6. Implement and test

```js
// Express-like sketch
const MAX_AGE = process.env.CORS_MAX_AGE || '600';
res.setHeader('Access-Control-Max-Age', MAX_AGE);
```

```bash
curl -sSI -X OPTIONS 'https://api.staging.example/v1/items' \
  -H 'Origin: https://app.staging.example' \
  -H 'Access-Control-Request-Method: PUT' \
  -H 'Access-Control-Request-Headers: authorization,content-type' \
  | rg -i 'max-age|allow-'
```

Browser: Network panel confirms single preflight per Max-Age window per tuple.

### 7. Document and hand off

1. Publish Max-Age defaults in API standards doc.
2. Link runbook to `cors-preflight-cache` for incidents.
3. Note interaction with service workers and multiple app tabs (each browser process caches preflights independently).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Allow-Headers | Fixed list | Reflect ACRH |
| Prod Max-Age | 600–3600 with change process | 86400 on week-1 API |
| Cross-origin need | Eliminate via same-site proxy when possible | CORS for everything “just in case” |
| Removal of header | Lower Max-Age first | Drop header while Max-Age=7200 |
| CDN | OPTIONS bypass | Cache OPTIONS globally |

## Output Checklist

- [ ] Call matrix: which requests preflight
- [ ] Same-site alternative considered
- [ ] Max-Age per environment documented
- [ ] Explicit Allow-Methods/Headers designed
- [ ] Vary and credentials policy aligned
- [ ] Rollout sequence for allowlist shrink/grow
- [ ] Staging browser verification done
- [ ] Config knobs (env) for emergency low Max-Age
- [ ] Incident runbook linked
- [ ] Residual OPTIONS load estimate accepted

## Rules

- Security of Origin validation outranks OPTIONS performance.
- Never “fix” CORS errors by `ACAO: *` with credentials.
- Design for change: long Max-Age is a commitment to header stability.
- Authorized systems only; keep skill focused on **design** of preflight caching policy.
