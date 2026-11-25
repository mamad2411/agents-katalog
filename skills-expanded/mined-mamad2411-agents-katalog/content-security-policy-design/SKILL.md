---
name: content-security-policy-design
description: >
  Design deployable Content-Security-Policy for owned web apps: nonces or hashes,
  strict-dynamic, script/style/img/connect sources, frame-ancestors, base-uri,
  report-uri/report-to, Report-Only staging, and rollout without breaking prod.
  Use for defense engineering — bypass research is content-security-policy-bypass.
---

# Content-Security-Policy Design

## Scope And Authorization

- **In scope:** web apps and CDNs you own.
- **Out of scope:** weakening CSP on third-party sites; shipping `'unsafe-inline'` permanently without risk acceptance.
- Always stage with **Content-Security-Policy-Report-Only** before enforce on complex apps.
- Pair with `code-quality-standards`, `clickjacking-defense-checklist` (`frame-ancestors`), and XSS prevention.

## When To Use

- Introducing or tightening CSP on SPAs or server-rendered apps.
- Moving off `'unsafe-inline'` to nonces/hashes/`strict-dynamic`.
- Tokens: CSP design, nonce, hash, strict-dynamic, report-to, script-src.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Authorized bypass testing | `content-security-policy-bypass` |
| XSS sink hunting | `xss-cross-site-scripting` |
| COOP/COEP isolation | `coop-coep-isolation` |
| Cookie flags | `cookie-security-flags` |

## Target End State (modern)

```http
Content-Security-Policy:
  default-src 'self';
  script-src 'nonce-{random}' 'strict-dynamic';
  style-src 'self' 'nonce-{random}';
  img-src 'self' data: https:;
  font-src 'self';
  connect-src 'self' https://api.example.com;
  object-src 'none';
  base-uri 'self';
  frame-ancestors 'none';
  form-action 'self';
  upgrade-insecure-requests
```

Adjust `connect-src` / `img-src` for real third parties; keep list minimal.

## Workflow

### 1. Inventory script & third-party surface

1. Inline scripts, event handler attributes, `eval`, `new Function`, template injection of JS.
2. Third-party tags (analytics, payments, chat).
3. Current CSP if any (header/meta).

```bash
curl -sI https://app.example.com/ | rg -i content-security-policy
```

### 2. Choose strategy

| App type | Strategy |
| --- | --- |
| SSR with templates | Per-request **nonce** on each script/style |
| Static hashed bundles | **Hashes** or nonces at edge |
| Heavy third-party | May need host allowlist + careful review; prefer loading via trusted nonced bootstrap + `'strict-dynamic'` |

### 3. Implement nonces (SSR sketch)

```html
<script nonce="{{ cspNonce }}">...</script>
<script src="/app.js" nonce="{{ cspNonce }}"></script>
```

```http
Content-Security-Policy: script-src 'nonce-...'; 'strict-dynamic'; object-src 'none'; base-uri 'self'
```

1. Nonce: high entropy, **per request**, not a static config value.
2. Do not place attacker-controlled content inside nonced inline scripts.
3. Remove inline event handlers (`onclick=`) → `addEventListener`.

### 4. Reporting and staging

```http
Content-Security-Policy-Report-Only: default-src 'self'; script-src 'nonce-...'; report-to csp-endpoint
Report-To: {"group":"csp-endpoint","max_age":10886400,"endpoints":[{"url":"https://csp.example.com/report"}]}
```

1. Collect violations 1–2 weeks; fix legitimate breaks.
2. Flip to enforcing CSP; keep reporting.
3. Alert on spike in violations after deploys.

### 5. Complementary directives

| Directive | Recommendation |
| --- | --- |
| `frame-ancestors` | `'none'` or allowlist — see clickjacking skills |
| `base-uri` | `'self'` or `'none'` |
| `object-src` | `'none'` |
| `form-action` | Limit where forms post |
| `worker-src` | Explicit if using workers |

### 6. Verify

1. Browser console: no unexpected blocks on critical flows (login, checkout).
2. Intentional XSS payload cannot run under enforce (lab).
3. `curl -sI` shows policy on all HTML entry routes (not only `/`).
4. CDN does not strip CSP on cache hits.

### 7. Hand off

1. Document allowed third parties + owners.
2. CI check for accidental `'unsafe-inline'` reintroduction.
3. Process for adding a new script host (security review).

## Rollout Phases

| Phase | Mode | Goal |
| --- | --- | --- |
| 0 | None | Inventory |
| 1 | Report-Only loose | Discover |
| 2 | Report-Only tight | Fix app |
| 3 | Enforce | Block XSS impact |
| 4 | Tighten further | Remove hosts |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Inline | Nonces/hashes | Permanent `'unsafe-inline'` |
| Nonce | Per request | Fixed `nonce=static` |
| Third parties | Minimal allowlist | `https:` for script-src |
| Rollout | Report-Only first | Enforce Friday evening blind |
| Coverage | All HTML responses | Only marketing homepage |

## Output Checklist

- [ ] Script/third-party inventory done
- [ ] Strategy (nonce/hash/strict-dynamic) chosen
- [ ] Report-Only collected and fixed
- [ ] Enforcing CSP deployed on all app HTML
- [ ] frame-ancestors/base-uri/object-src set
- [ ] Critical UX verified
- [ ] XSS residual tested in lab
- [ ] Third-party owner list maintained
- [ ] CI/regression against unsafe directives

## Rules

- Owned apps only for enforcement.
- Prefer fix app patterns over endless host allowlists.
- Evidence: headers + console + report volumes.
- Design/deploy skill; bypass assessment is the sibling.
