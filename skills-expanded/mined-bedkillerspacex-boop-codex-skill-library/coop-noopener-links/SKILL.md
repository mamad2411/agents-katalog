---
name: coop-noopener-links
description: >
  Harden outbound links and window.open on owned sites: default rel="noopener noreferrer"
  (and opener nulling) on target="_blank", reduce reverse-tabnabbing and referrer leakage,
  and align with Cross-Origin-Opener-Policy where relevant. Use when reviewing marketing
  sites, docs portals, CMS themes, SPAs, or email-rendered HTML that open third-party URLs.
---

# COOP / Noopener Links

## Scope And Authorization

- **In scope:** sites, apps, CMS themes, email templates, and design systems you own or are authorized to harden.
- **Out of scope:** injecting or testing link behavior on third-party properties without written authorization.
- Prefer non-production validation for CSP/COOP header experiments; ship link-rel defaults via normal frontend review.
- Redact user PII and session tokens from screenshots of Network/Console.
- Pair code changes with `code-quality-standards`.

## When To Use

- Inventory or fix `target="_blank"` / `window.open` without `rel="noopener"` (legacy browsers) or without modern defaults.
- Reduce **reverse tabnabbing** (`window.opener` navigation of the opener tab) and referrer leakage to third parties.
- Align link policy with `Cross-Origin-Opener-Policy` / `Cross-Origin-Embedder-Policy` work (see `cross-origin-opener-policy`).
- CMS/markdown pipelines that emit external anchors without sanitizing `rel` / `target`.
- Email or PDF-to-HTML exports that open external URLs in new tabs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full COOP / COEP / CORP isolation design | `cross-origin-opener-policy` |
| Content-Security-Policy nonces / report-only | `csp-nonce-rotation`, `csp-report-only-rollout` |
| CORS credentialed API misconfig | `cors-credentialed-requests` |
| Clickjacking / frame ancestors | matching frame-busting / CSP skill in catalog |
| Implementation quality baseline | `code-quality-standards` |

## Threat model (topic-specific)

| Risk | Mechanism | Mitigation |
| --- | --- | --- |
| Reverse tabnabbing | Opened page uses `window.opener.location` | `rel="noopener"` (or modern browser default) / `noopener` on `window.open` features |
| Referrer leakage | Full URL in `Referer` to third party | `rel="noreferrer"` or `Referrer-Policy` |
| Phishing UX | User thinks they are still on your origin | Clear external-link UI; prefer same-tab for untrusted deep links when product allows |
| User-content HTML | Stored XSS path + opener | Sanitize HTML; force `rel` on anchors server-side |
| Inconsistent stacks | React/Vue vs raw HTML vs markdown | Central link component + lint rule |

**Note on naming:** skill id includes `coop` historically; day-to-day work is **noopener/noreferrer on links**. Browser COOP headers are complementary isolation, not a substitute for safe external links.

## Modern browser defaults

- Chromium/Firefox/Safari treat `target="_blank"` as implying `noopener` in current versions; still set `rel` explicitly for:
  - Older WebViews and embedded browsers
  - Consistency, lintability, and CMS/email clients
  - Explicit `noreferrer` intent (noopener alone does not strip Referer in all cases)
- Prefer site-wide `Referrer-Policy: strict-origin-when-cross-origin` (or stricter) in addition to per-link `noreferrer` when product requires.

## Workflow

### 1. Confirm scope and success criteria

1. List surfaces: marketing HTML, app shell, docs (Docusaurus/MkDocs), CMS (WordPress/Contentful renderers), emails, mobile WebViews.
2. Success: no production `target="_blank"` without safe `rel`; shared `ExternalLink` component; lint/CI gate; optional Referrer-Policy header documented.
3. Note any intentional exceptions (e.g. first-party SSO popup that must retain `opener` for `postMessage` handshake) with owner + expiry.

### 2. Inventory current state

```bash
# Repo grep (adjust roots)
rg -n 'target=["'\'']_blank["'\'']' --glob '!node_modules' --glob '!dist'
rg -n 'window\.open\(' --glob '!node_modules'
rg -n 'rel=["'\''][^"'\'']*noopener' --glob '!node_modules' | head

# Live HTML sample (owned URL only)
curl -sS 'https://app.example.local/page' | rg -o 'target="_blank"[^>]*>' | head
```

1. Check markdown/MDX components and rich-text renderers for anchor props.
2. Check email templates and PDF HTML exporters separately (often miss frontend lint).
3. Record WebView / Electron shells that may ship older Chromium without noopener default.

### 3. Baseline

1. Capture sample vulnerable markup and a browser console check:
   - Open external link with `target="_blank"` only (if any remain).
   - From opened tab DevTools: `window.opener` should be `null` when policy is correct.
2. Note current `Referrer-Policy` and COOP response headers on the app origin.
3. Snapshot CI: is there an eslint rule or custom codemod already?

### 4. Apply hardening

#### HTML / templates

```html
<!-- Good -->
<a href="https://third-party.example/docs" target="_blank" rel="noopener noreferrer">
  External docs
</a>

<!-- Avoid for untrusted third parties -->
<a href="https://third-party.example" target="_blank">External</a>
```

#### window.open

```js
// Prefer explicit features; noopener prevents window.opener retention
const w = window.open(url, "_blank", "noopener,noreferrer");
// Defense in depth if a popup must be created another way:
if (w) w.opener = null;
```

#### React / design system

```tsx
type ExternalLinkProps = React.AnchorHTMLAttributes<HTMLAnchorElement> & {
  href: string;
};

export function ExternalLink({ href, children, ...rest }: ExternalLinkProps) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      {...rest}
    >
      {children}
    </a>
  );
}
```

#### Markdown / CMS post-process

- Force `rel="noopener noreferrer"` whenever `target="_blank"` or host ∉ first-party allowlist.
- Strip `javascript:` and data URLs in user-generated anchors (pair with XSS skill if needed).

#### Server-side Referrer-Policy (example nginx)

```nginx
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
# Optional isolation (coordinate with coop skill; can break OAuth popups)
# add_header Cross-Origin-Opener-Policy "same-origin" always;
```

### 5. Verify with evidence

```bash
# Static gate example (fail if _blank without noopener nearby — tune for false positives)
rg -n 'target="_blank"' -g '!node_modules' -g '!*.min.js' | rg -v 'noopener' || true

# Playwright / Cypress idea: open page, click external link, assert opener is null
# (implement in your e2e suite on staging)
```

Manual:

1. Chrome DevTools → open external link → in new tab Console: `window.opener` → `null`.
2. Network tab: cross-origin navigation Referer matches policy (full path not leaked if noreferrer/strict policy).
3. Regression: intentional OAuth/`postMessage` popups that need `opener` still work; document them as exceptions.

### 6. Observe and harden

1. Add eslint-plugin rules or custom AST lint for `target="_blank"` without `noopener`.
2. Code review checklist item for new marketing pages and CMS modules.
3. Re-check after framework upgrades (link components sometimes reset defaults).

### 7. Hand off

1. Document the canonical `ExternalLink` component path and exceptions list.
2. Link tickets for remaining CMS/email surfaces.
3. Apply `code-quality-standards` for any shared component.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| External tab | `rel="noopener noreferrer"` | Bare `target="_blank"` in WebViews |
| Popup API | `window.open(url, "_blank", "noopener,noreferrer")` | `window.open(url)` then trust opener |
| UGC HTML | Server sanitizer forces `rel` | Trust client-only Markdown |
| Referrer | Site `Referrer-Policy` + noreferrer for sensitive paths | Leak session IDs in query strings via Referer |
| Exceptions | Named SSO popup + owner | Global “we need opener” without list |

## Output Checklist

- [ ] Scope/surfaces listed (app, docs, CMS, email, WebView)
- [ ] Inventory of `target="_blank"` / `window.open` completed
- [ ] Shared component or template default ships `noopener noreferrer`
- [ ] User-content / markdown pipeline forces safe `rel`
- [ ] Referrer-Policy considered site-wide
- [ ] COOP header work routed or explicitly deferred
- [ ] Lint/CI or e2e evidence for opener null
- [ ] Documented exceptions (OAuth popups, etc.) with owners
- [ ] `code-quality-standards` applied to shared link helpers
- [ ] Residual risk noted (old WebViews, email clients)

## Rules

- Authorized properties only; do not probe third-party sites for opener behavior without scope.
- Prefer explicit `rel` even when browsers default noopener — WebViews and email lag.
- Do not set COOP `same-origin` blindly; it can break legitimate cross-origin window flows — use `cross-origin-opener-policy` for that design.
- Never put session tokens in URLs that third parties may receive via Referer.
- Keep this skill focused on link/`window.open` opener and referrer hygiene; route full isolation headers and CORS elsewhere.
---

# Note

Skill id `coop-noopener-links` covers **noopener/noreferrer link hygiene** first; treat COOP headers as adjacent.
