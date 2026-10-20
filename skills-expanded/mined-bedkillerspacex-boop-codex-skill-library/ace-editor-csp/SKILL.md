---
name: ace-editor-csp
description: >
  Content-Security-Policy hardening for Ace Editor and similar in-browser code editors
  (Ace, CodeMirror 5/6, Monaco): script/worker origins, unsafe-eval trade-offs, blob/data
  workers, style sources, and XSS surface when embedding user code. Use for owned web IDEs,
  admin script consoles, and CMS code fields — not for weakening CSP on unrelated third-party sites.
---

# Ace / Code Editor CSP

## Scope And Authorization

- **In scope:** web applications you own that embed Ace, CodeMirror, Monaco, or similar editors.
- **Out of scope:** advising attackers on bypassing CSP on targets without authorization.
- Prefer staging for CSP enforcement experiments (`Content-Security-Policy-Report-Only` first).
- Redact customer code samples that contain secrets when filing bugs.
- Pair app changes with `code-quality-standards`.

## When To Use

- Embedding Ace Editor (or peers) and CSP breaks workers, themes, or syntax highlight.
- Moving off `unsafe-inline` / `unsafe-eval` while keeping the editor usable.
- Reviewing XSS risk of **user-controlled code** displayed or executed in-browser.
- Designing CSP for online judges, low-code tools, or admin “script” panes.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General XSS testing | `xss-cross-site-scripting` |
| Broad frontend a11y | `accessibility-a11y-checklist` |
| Electron shell hardening | `electron` / electron security skills |
| API authz | `api-auth-and-jwt-abuse` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Editor | Typical CSP friction |
| --- | --- |
| Ace | WebWorkers for modes; dynamic `eval`-like paths in older builds; CDN script paths |
| CodeMirror 5 | `eval` in some runmodes; iframe options |
| CodeMirror 6 | Modular; better CSP story if bundled; still worker/blob needs |
| Monaco | Web workers (`blob:` or same-origin worker bundles); loader config |

**Key directives:** `script-src`, `worker-src`, `style-src`, `img-src` (gutter icons), `font-src`, `connect-src` (if LSPs), `frame-src` (sandboxed previews).

## Workflow

### 1. Confirm scope and success criteria

1. Record app routes with editors, user-generated vs staff-only, CSP delivery (header vs meta).
2. Success: editor loads (highlight, worker, resize); CSP has **no** unbounded `unsafe-inline`/`unsafe-eval` unless ticketed exception; user code not executed in privileged origin without sandbox.
3. Inventory script supply: npm bundle vs CDN.

### 2. Baseline CSP and console errors

```bash
curl -sSI 'https://app.example/editor' | grep -i content-security-policy
# Browser: DevTools → Console for CSP violations; Network for worker loads
```

1. Capture violations: blocked worker, blocked inline style, blocked `eval`.
2. Note dual headers (enforce + report-only).

### 3. Bundle strategy (preferred over CDN + wildcards)

```bash
# Example: package editor into same-origin static assets
npm install ace-builds
# Serve /static/ace/** from your origin; pin versions in lockfile
```

| Approach | CSP impact |
| --- | --- |
| Same-origin bundled workers | `worker-src 'self'` |
| `blob:` workers | need `worker-src blob:` (or `script-src` legacy browsers) |
| CDN scripts | `script-src https://cdn.example` tightly pinned |
| Inline config bootstrapping | prefer external file or nonce |

### 4. Craft CSP for editor pages

**Report-only first:**

```http
Content-Security-Policy-Report-Only:
  default-src 'self';
  script-src 'self' 'nonce-RANDOM';
  worker-src 'self' blob:;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data:;
  font-src 'self' data:;
  connect-src 'self';
  object-src 'none';
  base-uri 'self';
  frame-ancestors 'none';
  report-uri /csp-report
```

Notes:

1. Ace themes often need **`style-src` inline** or hashes for injected `<style>`; prefer hashed styles or CSS files extracted at build.
2. Prefer **nonces** on bootstrap scripts over `unsafe-inline`.
3. Avoid `unsafe-eval` — upgrade editor build or disable features that require it; if unavoidable, isolate editor to a tightly scoped origin/path and document risk.
4. `worker-src` falls back to `script-src` in older browsers — test both.

### 5. Execution and XSS boundaries

| Scenario | Safe pattern |
| --- | --- |
| Syntax highlight only | Treat content as text; never `innerHTML` user code into privileged DOM |
| Live preview HTML | Separate `sandbox` iframe with **null origin** or distinct origin; restrictive CSP on iframe doc |
| Run user JS | Dedicated sandbox origin; no parent cookies; `postMessage` allowlist |
| Admin server-side script | Never execute admin paste in other users’ browsers |

```javascript
// Bad: privileged page
el.innerHTML = userCode
// Better: text content / editor setValue only
ace.edit(el).session.setValue(userCode)
```

### 6. Verify

```bash
# Header present and not report-only only (when enforcing)
curl -sSI 'https://staging.example/editor' | grep -i content-security-policy

# Manual: open editor, change mode, open find, resize — no CSP errors
# Manual: paste <script>alert(1)</script> as code text — must NOT execute in parent
```

1. Run axe only as secondary; CSP is not an a11y issue.
2. Regression: CSP report endpoint volume after deploy.

### 7. Hand off

1. Document required directives per editor version.
2. Ticket any residual `unsafe-eval` with owner and upgrade plan.
3. Ensure CI checks headers on editor routes (smoke).

## Directive Cheat Sheet

| Directive | Editor-related guidance |
| --- | --- |
| `script-src` | `'self'` + nonces; pin CDNs; avoid `*` |
| `worker-src` | `'self'` and/or `blob:` as required by build |
| `style-src` | Prefer files/hashes; document if `'unsafe-inline'` for themes |
| `frame-src` | Only preview sandbox origins |
| `connect-src` | LSP/websocket endpoints explicit |
| `object-src` | `'none'` |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Loading | Same-origin version-pinned assets | `script-src * 'unsafe-inline' 'unsafe-eval'` |
| Workers | Known `worker-src` | Silent fail, half-broken highlight ignored |
| User code | Text in editor only | `eval(userCode)` on main origin |
| Rollout | Report-Only → enforce | Enforce broken CSP on Friday prod |
| Secrets | Code samples scrubbed | Customer API keys in bug screenshots |

## Output Checklist

- [ ] Editor products/versions and pages inventoried
- [ ] Baseline CSP + violation log captured
- [ ] Bundle/CDN strategy chosen
- [ ] `script-src` / `worker-src` / `style-src` tuned
- [ ] XSS boundary for user code documented (sandbox if execute)
- [ ] Staging functional test of editor features
- [ ] Enforcement plan + report monitoring
- [ ] Residual exceptions ticketed with expiry
- [ ] `code-quality-standards` applied to app changes

## Rules

- Owned apps only; do not weaken others’ CSP.
- Prefer removing `unsafe-eval` over documenting it forever.
- Never run untrusted code in a context that holds session cookies.
- Keep editor CSP changes scoped; do not casually open `script-src` globally.
- Redact secrets in sample code and reports.
