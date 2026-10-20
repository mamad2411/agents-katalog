---
name: csp-nonce-rotation
description: >
  Implement per-request Content-Security-Policy nonces for scripts (and styles)
  on owned web apps: cryptographically strong nonce generation, CSP header
  binding, template injection of nonce attributes, and avoiding nonce reuse or
  leakage. Use when removing unsafe-inline, adopting strict-dynamic, or fixing
  static nonces that never rotate.
---

# CSP Nonce Rotation

## Scope And Authorization

- **In scope:** First-party web apps and SSR templates you control.
- **Out of scope:** Breaking third-party sites' CSP; intentionally shipping XSS.
- Stage CSP with report-only when needed (`csp-report-only-rollout`).
- Pair with XSS prevention — CSP is defense-in-depth, not a substitute for output encoding.

## When To Use

- Migrating off `'unsafe-inline'` for `script-src` / `style-src`.
- SSR frameworks (Rails, Django, ASP.NET, Next custom server) that can set per-request CSP.
- Adopting `'strict-dynamic'` with nonces.
- Fixing misimplementations: fixed nonce in config, nonce in static HTML cache, or nonce logged publicly.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Report-Only rollout / collectors | `csp-report-only-rollout` |
| XSS exploit validation | `xss-cross-site-scripting` |
| Hash-only CSP for static sites | CSP hash workflow / static hosting guides |
| COOP isolation | `cross-origin-opener-policy` |
| Implementation quality baseline | `code-quality-standards` |

## Nonce requirements

| Rule | Why |
| --- | --- |
| Cryptographically random | Predictable nonces defeat CSP |
| Per-request (or per-response) | Reuse allows attacker to replay nonce in injection |
| Bound into CSP header **and** tags | Mismatch blocks legit scripts |
| Not cached across users | Shared HTML cache + unique CSP breaks or leaks |
| Sufficient length | e.g. 128 bits+ raw → base64 |

## Workflow

### 1. Confirm scope and success criteria

1. Pages with inline scripts/styles inventory; CDN third parties.
2. Success: unique nonce each response; inline scripts use `nonce=`; CSP drops unsafe-inline; app functions; XSS still encoded.

### 2. Baseline current CSP

```bash
curl -sSI 'https://app.example.local/' | rg -i 'content-security-policy'
# Browser console CSP errors sample
```

### 3. Generate nonce per request

```js
// Node/Express sketch
const crypto = require('crypto');
app.use((req, res, next) => {
  const nonce = crypto.randomBytes(16).toString('base64');
  res.locals.cspNonce = nonce;
  res.setHeader(
    'Content-Security-Policy',
    `default-src 'self'; script-src 'nonce-${nonce}' 'strict-dynamic'; object-src 'none'; base-uri 'self'`
  );
  next();
});
```

```csharp
// ASP.NET middleware sketch
var nonce = Convert.ToBase64String(RandomNumberGenerator.GetBytes(16));
httpContext.Items["csp-nonce"] = nonce;
httpContext.Response.Headers.ContentSecurityPolicy =
    $"default-src 'self'; script-src 'nonce-{nonce}' 'strict-dynamic'; object-src 'none'; base-uri 'self'";
```

### 4. Emit nonce on tags

```html
<script nonce="<%= cspNonce %>">
  // inline boot only if necessary
</script>
<script src="/assets/app.js" nonce="<%= cspNonce %>"></script>
```

Notes:

1. With `'strict-dynamic'`, trust propagates to scripts loaded by nonced scripts (browser-dependent details — verify).
2. External scripts may still need host allowlists on older browsers without strict-dynamic support — progressive policy design.
3. Prefer external files + nonces/hashes over large inline blocks.

### 5. Caching and CDN pitfalls

| Setup | Risk | Mitigation |
| --- | --- | --- |
| CDN caches HTML | Nonce/header mismatch | Bypass cache for HTML or use edge worker to inject matching pair |
| Shared page cache | User A nonce served to B | Private/no-store for nonced HTML or edge rewrite |
| Static export only | Cannot per-request nonce | Use hashes for static inline or eliminate inline |

### 6. Verify rotation

```bash
# Two fetches must show different nonces
curl -sSI 'https://app.example.local/' | rg -i 'content-security-policy'
curl -sS 'https://app.example.local/' | rg -o 'nonce="[^"]+"' | head
# Confirm header nonce matches HTML nonce
```

Browser: legit app scripts run; injected `<script>alert(1)</script>` without nonce blocked.

### 7. Operate

1. Do not log full CSP nonces next to user HTML if that aids attackers (low risk alone, still avoid noise).
2. Monitor CSP violation reports after enforce.
3. Document how designers add new inline scripts (they should not — use bundles).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Nonce value | 16+ random bytes / request | `nonce-abc123` fixed in env |
| Header | Same nonce as tags | Header only, tags missing |
| Cache | HTML uncached or edge-paired | Global CDN HTML + dynamic CSP |
| Policy | Drop unsafe-inline when nonced | Nonce + unsafe-inline forever |
| XSS | Still HTML-encode | Rely on CSP alone |

## Output Checklist

- [ ] Inline script inventory done
- [ ] CSPRNG nonce per response
- [ ] CSP header includes `'nonce-…'`
- [ ] Templates set matching `nonce` attributes
- [ ] Cache strategy safe for nonces
- [ ] unsafe-inline removed or ticketed residual
- [ ] Dual-response rotation verified
- [ ] Browser functional test + blocked inject test
- [ ] Report-only path used if first rollout
- [ ] Residual third-party script plan documented

## Rules

- Nonce reuse or static nonces are failures.
- CSP complements, never replaces, output encoding.
- Authorized apps only; focus on **per-request CSP nonce rotation**.
