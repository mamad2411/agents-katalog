---
name: cors-null-origin-deny
description: >
  Deny or tightly control CORS for Origin: null on owned APIs. Use when assessing
  sandboxed iframes, file:// / data: / unique opaque origins, redirect chains that
  yield null, or allowlists that treat the literal string "null" as trusted —
  especially with Access-Control-Allow-Credentials.
---

# CORS Null Origin Deny

## Scope And Authorization

- **In scope:** APIs and browser apps you own or are authorized to test/harden.
- **Out of scope:** Exploiting null-Origin CORS on third-party sites without authorization.
- Prefer staging; use synthetic sandboxed pages you control for PoCs.
- Redact cookies and tokens from evidence.
- Pair with `code-quality-standards` and `cors-credentialed-requests` when ACAC is involved.

## When To Use

- API returns `Access-Control-Allow-Origin: null` (literal).
- Allowlist includes `"null"` or treats missing/empty Origin loosely.
- Product embeds untrusted content in sandboxed iframes without `allow-same-origin`.
- Investigating attacks via local HTML files, PDF viewers, or privacy-sensitive redirects.
- Hardening policy: default deny for null Origin on authenticated APIs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General CORS triage | `cors-cross-origin-misconfiguration` |
| Credentialed CORS deep-dive | `cors-credentialed-requests` |
| Full org checklist | `cors-security-checklist` |
| Preflight Max-Age | `cors-preflight-cache-design` |
| Implementation quality baseline | `code-quality-standards` |

## Why `Origin: null` appears

| Source | Notes |
| --- | --- |
| Sandboxed iframe | `sandbox` without `allow-same-origin` → opaque origin serializes as `null` |
| `file://` pages | Many browsers send `Origin: null` on some requests |
| `data:` / `blob:` navigations | Opaque origins |
| Privacy redirects / some cross-origin chains | Implementation-dependent |
| Attacker-controlled local HTML | User opens malicious file that calls your API |

If the server **reflects** `ACAO: null` with **ACAC: true**, a page in an opaque origin can read credentialed responses when cookies are still sent (subject to SameSite / third-party cookie rules).

## Workflow

### 1. Confirm scope and success criteria

1. Identify cookie-authenticated APIs vs public endpoints.
2. Success: production authenticated APIs never emit `ACAO: null`; automated test covers `Origin: null`; any intentional null allowance is non-credentialed and documented.

### 2. Probe null Origin

```bash
API='https://api.example.local/v1/me'
curl -sSI -H 'Origin: null' "$API" | rg -i 'HTTP/|access-control|vary'
curl -sSI -X OPTIONS "$API" \
  -H 'Origin: null' \
  -H 'Access-Control-Request-Method: GET' \
  -H 'Access-Control-Request-Headers: content-type' | rg -i 'access-control|HTTP/'
```

Compare with a valid SPA origin and an evil origin.

### 3. Code review for null trust

```bash
rg -n '"null"|Origin.*null|AllowAnyOrigin|SetIsOriginAllowed' --glob '!node_modules'
```

Flags:

- Explicit allowlist entry `"null"`.
- Framework “allow all” that stringifies null.
- Logic: `if (origin) allow(origin)` without rejecting the string `null`.

### 4. Browser PoC sketch (authorized, test account)

```html
<iframe
  sandbox="allow-scripts"
  srcdoc="
    <script>
      fetch('https://api.example.local/v1/me', { credentials: 'include' })
        .then(r => r.text()).then(t => parent.postMessage(t, '*'))
        .catch(e => parent.postMessage(String(e), '*'));
    </script>
  "
></iframe>
<script>
window.addEventListener('message', e => console.log('from sandbox', e.data));
</script>
```

Host only on controlled infra. Interpret results alongside SameSite cookie policy (third-party/sandboxed contexts may not send cookies).

### 5. Harden

```js
const ALLOW = new Set(['https://app.example.com']);
function isAllowedOrigin(origin) {
  if (!origin || origin === 'null') return false;
  return ALLOW.has(origin);
}
```

1. Do **not** set ACAO when origin is null or unlisted.
2. Never pair `ACAO: null` with `ACAC: true` on sensitive APIs.
3. Prefer first-party iframes with explicit origins for trusted embeds; avoid relying on null.
4. Document rare exceptions (e.g. local dev tools) for non-prod only.

### 6. Verify

```bash
# Expect no ACAO: null on authenticated API
curl -sSI -H 'Origin: null' "$API" | rg -i 'access-control-allow-origin' || echo 'No ACAO (good)'
# Allowed origin still works
curl -sSI -H 'Origin: https://app.example.com' "$API" | rg -i 'access-control'
```

Add CI assertion: response to `Origin: null` must not include `Access-Control-Allow-Origin: null` for protected routes.

### 7. Hand off

1. Broader reflection issues → `cors-cross-origin-misconfiguration`.
2. Cookie SPA design → `cors-credentialed-requests` + CSRF skills.
3. Record residual risk if product must support sandboxed partner widgets (prefer token-in-postMessage, not cookie CORS to null).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| null policy | Deny on auth APIs | `ACAO: null` + ACAC true |
| Embeds | Trusted origin iframe | Sandbox without plan + cookie API |
| Allowlist | Exact https origins | `"null"` in prod allowlist |
| Tests | Origin null case in CI | Only test happy SPA origin |
| Dev | Localhost explicit origin | Copy dev “allow all” to prod |

## Output Checklist

- [ ] Auth APIs probed with `Origin: null`
- [ ] ACAO/ACAC recorded for null vs allowlisted
- [ ] Code paths that allow null identified or absent
- [ ] Hardening applied (reject null)
- [ ] Regression test added
- [ ] Sandbox/iframe product cases documented
- [ ] SameSite interaction noted
- [ ] Redacted evidence stored
- [ ] Sibling CORS handoffs done
- [ ] Residual exceptions have owners

## Rules

- Authorized testing only.
- Treat literal `null` as untrusted, not as “no origin.”
- Opaque-origin browser behavior varies — verify with real browsers for PoCs.
- Keep this skill focused on **null Origin** deny/allow policy; route general CORS elsewhere.
