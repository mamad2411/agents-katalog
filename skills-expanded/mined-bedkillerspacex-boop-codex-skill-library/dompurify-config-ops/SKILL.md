---
name: dompurify-config-ops
description: >
  Operate DOMPurify safely for user-generated HTML: ALLOWED_TAGS/ATTR, URI hooks, whole-
  document mode, SAFE_FOR_TEMPLATES, clobber mitigation (id/name), and upgrade discipline.
  Use when DOMPurify config, sanitize UGC rich text, XSS filter bypass review, or hardening
  client-side HTML sanitization on owned apps — not as a substitute for output encoding
  everywhere or server-side policy alone.
---

# DOMPurify Config Ops

## Scope And Authorization

- **In scope:** Frontends and sanitization configs you own; authorized bypass testing on your apps.
- **Out of scope:** Crafting bypasses for third-party sites without authorization.
- Prefer server-side sanitization for high-risk UGC when possible; DOMPurify is defense-in-depth in browser or isomorphic use.
- Keep DOMPurify version patched—bypasses get fixed in releases.
- Pair with `xss-cross-site-scripting`, `dom-clobbering-awareness`, `dom-clobbering-forms`, and `code-quality-standards`.

## When To Use

- Rendering markdown/HTML comments, bios, CMS blocks.
- Configuring or reviewing `DOMPurify.sanitize(dirty, config)`.
- After XSS or DOM clobber findings involving rich text.
- Choosing between tag allowlists for marketing CMS vs strict comments.
- Adding hooks to validate URLs (`javascript:` rejection already default—verify).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full XSS methodology | `xss-cross-site-scripting` |
| DOM clobber patterns | `dom-clobbering-awareness` / `dom-clobbering-forms` |
| CSP deployment | security header skills |
| React `dangerouslySetInnerHTML` patterns | React security + this skill |
| Code quality baseline | `code-quality-standards` |

## Defaults vs config

DOMPurify ships secure defaults for many cases; **custom allowlists** are the usual foot-gun (`ADD_TAGS`, `ADD_ATTR`, `ALLOW_UNKNOWN_PROTOCOLS`).

| Config area | Guidance |
| --- | --- |
| `ALLOWED_TAGS` | Minimal set for use case |
| `ALLOWED_ATTR` | Avoid event handlers; careful with `style` |
| `ALLOW_DATA_ATTR` | Often false unless needed |
| `ADD_TAGS` / `ADD_ATTR` | Review every addition as security change |
| `WHOLE_DOCUMENT` / `RETURN_DOM` | Know sink (innerHTML vs node) |
| Hooks | `uponSanitizeAttribute` for URL policy |
| `SANITIZE_DOM` | Related to clobber mitigation—keep enabled unless expert reason |

## Workflow

### 1. Confirm scope and success criteria

1. UGC types (comment vs CMS), browsers, whether sanitize is client, server (jsdom), or both.
2. Success: XSS test suite fails to execute script; clobber ids stripped or harmless; version pinned; config reviewed.
3. Owner for allowlist changes.

### 2. Inventory usage

```bash
rg -n "DOMPurify|dompurify|sanitize\\(" -g '*.{js,ts,tsx,jsx,vue}'
```

1. List each call site and config object.
2. Note post-processing that re-adds HTML after sanitize (critical bug).

### 3. Define profiles

```javascript
// Strict comments
export const PURIFY_COMMENT = {
  ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "code", "pre", "p", "br", "ul", "ol", "li"],
  ALLOWED_ATTR: ["href", "title", "rel"],
  ALLOW_DATA_ATTR: false,
};

// Optional: force rel on anchors via hook
```

```javascript
// CMS may need more tags — separate profile + review process
export const PURIFY_CMS = {
  ALLOWED_TAGS: [/* ... */],
  ALLOWED_ATTR: [/* ... */],
};
```

1. Never one global loose config for all surfaces.
2. Strip `id`/`name` if clobber is a concern:

```javascript
DOMPurify.addHook("uponSanitizeAttribute", (node, data) => {
  if (data.attrName === "id" || data.attrName === "name") {
    data.keepAttr = false;
  }
});
```

### 4. URL and URI safety

1. Allow only `http:`, `https:`, `mailto:` as needed—reject `javascript:`, data unless carefully constrained.
2. For `href`/`src`, use hooks to enforce https allowlist domains if product requires.
3. Be careful with SVG/MathML allowlists—historically higher complexity.

### 5. Integration patterns

```javascript
import DOMPurify from "dompurify";

export function safeHtml(dirty) {
  return DOMPurify.sanitize(dirty, PURIFY_COMMENT);
}

// React
<div dangerouslySetInnerHTML={{ __html: safeHtml(userHtml) }} />
```

1. Sanitize **immediately before** insert; do not store only dirty and trust later.
2. If isomorphic, ensure same version/config on server and client.
3. CSP as additional layer (`script-src`)—not a replacement for sanitize.

### 6. Test for regressions and bypasses (authorized)

```javascript
const payloads = [
  `<img src=x onerror=alert(1)>`,
  `<svg/onload=alert(1)>`,
  `<a href="javascript:alert(1)">x</a>`,
  `<form id="config"><input name="x"></form>`,
];
for (const p of payloads) {
  const out = DOMPurify.sanitize(p, PURIFY_COMMENT);
  // assert no event handlers / javascript: / forbidden tags
}
```

1. Upgrade DOMPurify promptly; read changelogs for security fixes.
2. Optional: add known public XSS vectors as unit fixtures (safe asserts on output string).

### 7. Operate and hand off

1. Dependabot on `dompurify` (`dependabot-config-hardening`).
2. CODEOWNERS for purify config files.
3. Document how editors map to tags (WYSIWYG → allowlist).
4. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Allowlist | Minimal per surface | ADD_TAGS freely |
| Version | Pinned + updated | Years-old DOMPurify |
| Order | Sanitize then insert | Insert then “clean” |
| Clobber | Strip id/name | Allow all attrs |
| SVG | Off unless needed | Full SVG UGC |
| Tests | Payload fixtures | Hope |

## Output Checklist

- [ ] All sanitize call sites inventoried
- [ ] Per-surface profiles defined
- [ ] id/name/clobber policy set
- [ ] URL hooks/policies reviewed
- [ ] No post-sanitize HTML concatenation of dirty data
- [ ] Unit fixtures for XSS/clobber samples
- [ ] DOMPurify version pinned and update path live
- [ ] CSP considered as defense-in-depth
- [ ] Owners for allowlist changes
- [ ] Residual risk documented

## Rules

- Custom allowlists are security-sensitive code.
- Keep library updated; follow security releases.
- Sanitize at the boundary; encode elsewhere as appropriate.
- Authorized bypass testing only on owned apps.
- DOMPurify is not a free pass for `innerHTML` of unvetted complex SVG without review.
