---
name: cors-preflight-cache
description: >
  Operate and troubleshoot browser CORS preflight caching via Access-Control-Max-Age,
  including options request volume, stale policy after CORS changes, and CDN interaction
  with OPTIONS. Use on owned APIs when preflight storms, Max-Age mis-sets, or post-deploy
  clients still use old CORS allow headers.
---

# CORS Preflight Cache

## Scope And Authorization

- **In scope:** APIs and edge configs you operate; performance and correctness of OPTIONS / Max-Age.
- **Out of scope:** Turning preflight cache into a security bypass narrative without evidence; attacking third-party APIs.
- Prefer staging load tests for OPTIONS rate changes.
- Redact auth headers from traces.
- Pair with `cors-preflight-cache-design` for greenfield TTL policy and `code-quality-standards` for middleware changes.

## When To Use

- High rate of `OPTIONS` on API gateways after SPA deploy.
- Clients fail CORS after you tightened Allow-Headers/Methods until browser restart / Max-Age expiry.
- CDN caches OPTIONS responses incorrectly (wrong ACAO).
- Debugging `Access-Control-Max-Age` values already shipped.
- Distinguishing browser preflight cache from HTTP Cache-Control on GET responses.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Choosing TTLs and policy design from scratch | `cors-preflight-cache-design` |
| Origin reflection / ACAC bugs | `cors-cross-origin-misconfiguration`, `cors-credentialed-requests` |
| General HTTP caching / CDN for GET bodies | caching-strategies or CDN skills |
| Security checklist pass | `cors-security-checklist` |
| Implementation quality baseline | `code-quality-standards` |

## Concepts

| Layer | What is cached | Who caches |
| --- | --- | --- |
| Browser preflight cache | Successful OPTIONS result for origin+URL+method+headers tuple | Browser, duration ≤ Max-Age (and browser caps) |
| HTTP shared cache / CDN | OPTIONS or GET responses if Cache-Control allows | Edge; dangerous if ACAO varies without Vary |
| App authz cache | Unrelated | Do not confuse with CORS |

Browsers cap Max-Age (historically ~2h in Chrome for some cases; treat multi-day values as “long” and verify current engine behavior).

## Workflow

### 1. Confirm scope and success criteria

1. List endpoints that trigger preflight (custom headers, non-simple methods, JSON content-types).
2. Success: OPTIONS rate within budget; CORS policy changes take effect within agreed Max-Age; no cross-origin cache bleed.

### 2. Inventory current Max-Age and OPTIONS behavior

```bash
API='https://api.example.local/v1/items'
curl -sSI -X OPTIONS "$API" \
  -H 'Origin: https://app.example.com' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type,authorization' \
  | rg -i 'HTTP/|access-control|cache-control|vary|age'
```

Record: `Access-Control-Max-Age`, allow lists, `Vary`, CDN `Age`/`X-Cache`.

### 3. Baseline traffic

1. Gateway metrics: count OPTIONS vs GET/POST per route.
2. Browser DevTools: first request shows preflight; repeat within Max-Age should skip OPTIONS (same tuple).
3. After CORS config change: note how long clients keep old behavior.

### 4. Operational fixes

#### Stale preflight after security tighten

1. Temporarily set `Access-Control-Max-Age` low (e.g. 60–600) during rollout.
2. Ensure new Allow-Headers/Methods are correct before raising Max-Age again.
3. Communicate that open tabs may cache preflight until expiry — hard refresh does not always clear preflight cache in all browsers; Max-Age expiry or browser restart may be needed.

#### OPTIONS storms

1. Confirm SPA is not sending avoidable non-simple requests (extra custom headers on every call).
2. Raise Max-Age only after allowlists are stable (see design skill).
3. Ensure load balancer does not disable connection reuse in a way that multiplies handshakes (orthogonal but compounds pain).

#### CDN caching OPTIONS

```text
# Dangerous pattern: CDN caches OPTIONS with ACAO for origin A, serves to origin B
# Mitigations: do not cache OPTIONS at CDN; or Vary: Origin, Access-Control-Request-Method, Access-Control-Request-Headers
```

Prefer: CDN bypass for OPTIONS, or origin-generated OPTIONS with correct Vary and short edge TTL.

### 5. Verify

```bash
# Before/after Max-Age
curl -sSI -X OPTIONS "$API" \
  -H 'Origin: https://app.example.com' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type' \
  | rg -i 'max-age|allow-origin|allow-headers|vary'

# Confirm disallowed origin still has no privilege
curl -sSI -X OPTIONS "$API" \
  -H 'Origin: https://evil.example' \
  -H 'Access-Control-Request-Method: POST' | rg -i 'access-control'
```

Browser check: two identical POSTs; second without OPTIONS when Max-Age active.

### 6. Observe

1. Alert on OPTIONS ratio spikes (may indicate client bug or Max-Age=0 regression).
2. After CORS PR merges, watch error rates for “CORS missing Allow-Header” for Max-Age window.
3. Document browser cap differences for support teams.

### 7. Hand off

- Policy numbers and SPA header minimization → `cors-preflight-cache-design`.
- Security of Origin allowlist → other CORS skills.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| During break-glass CORS fix | Low Max-Age | Max-Age 86400 on wrong Allow-Headers |
| CDN | Bypass OPTIONS or strict Vary | Cache OPTIONS without Vary Origin |
| Metrics | OPTIONS rate dashboard | Ignore OPTIONS in SLOs |
| Security change | Assume clients may lag Max-Age | Assume instant global enforcement |
| Debugging | Separate preflight cache vs GET cache | Blame Redis for browser OPTIONS |

## Output Checklist

- [ ] Preflight-triggering routes listed
- [ ] Current Max-Age and Allow-* captured
- [ ] OPTIONS volume baselined
- [ ] CDN OPTIONS behavior reviewed
- [ ] Operational Max-Age adjustment applied if needed
- [ ] Verification of skip-preflight and deny evil Origin
- [ ] Rollout notes for stale preflight window
- [ ] Design skill handoff if TTL strategy unclear
- [ ] Monitoring for OPTIONS ratio
- [ ] Residual browser-cap notes

## Rules

- Preflight cache is not a substitute for correct ACAO/ACAC policy.
- Do not raise Max-Age to hide origin overload without fixing chatty clients.
- Authorized APIs only.
- Focus here is **operating/troubleshooting** preflight cache; design skill owns greenfield TTL choice.
