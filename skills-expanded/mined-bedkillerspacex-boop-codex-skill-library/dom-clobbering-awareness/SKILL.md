---
name: dom-clobbering-awareness
description: >
  Authorized DOM clobbering awareness: named HTML elements (id/name) shadowing window and
  document properties, form/collection multi-level clobbering, and client config or sink
  confusion without a script injection. Use when markup accepts attacker-controlled id/name
  attributes, JS reads bare globals or document.* as config, or reviews mix DOM clobbering
  with XSS or prototype pollution during authorized web assessments.
---

# DOM Clobbering Awareness

## Scope And Authorization

- **In scope:** Web apps you own or test under written authorization.
- **Out of scope:** Attacking third-party sites; weaponizing clobbering for drive-by abuse outside RoE.
- Prefer code review + controlled PoC on staging; avoid production payload noise.
- Redact session tokens in PoC HTML.
- Pair with `dom-clobbering-forms`, `xss-cross-site-scripting`, `dompurify-config-ops`, and `code-quality-standards`.

## When To Use

- Markup allows user-controlled `id` / `name` without sanitization.
- JS uses bare identifiers (`config`, `defaultView`) or `document.foo` expecting built-ins/objects.
- Reviewing filters that strip `<script>` but allow anchors/forms/images with names.
- Explaining findings that are not classic XSS yet still rewrite program state.
- Training developers on named-element globals in HTML documents.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Form/anchor multi-level chains detail | `dom-clobbering-forms` |
| Classic script XSS | `xss-cross-site-scripting` |
| HTML sanitizer config | `dompurify-config-ops` |
| Prototype pollution | JS prototype pollution skills |
| Code quality baseline | `code-quality-standards` |

## Core idea

In HTML documents, elements with `id` or certain `name` values can surface as properties on `window` / `document`. Script that treats those properties as trusted objects/config can be **clobbered** by attacker markup—often without executing a script tag.

```html
<!-- Attacker-controlled HTML without <script> -->
<a id="config" href="https://evil.example"></a>
```

```javascript
// Vulnerable pattern: expects config object, gets HTML element
if (config.url) {
  location.href = config.url; // may coerce unexpectedly
}
```

| Pattern | Risk |
| --- | --- |
| Bare global as config | Element replaces object |
| `document.getElementById` skipped for `document.x` | Named access returns element |
| Sanity checks `typeof x === "object"` | Elements are objects |
| `x?.value` / form controls | Nested clobber via forms (`dom-clobbering-forms`) |

## Workflow

### 1. Confirm scope and success criteria

1. Where user HTML/SVG is rendered (comments, markdown, CMS, email HTML).
2. Success: inventory of clobberable sinks; PoC or code proof; sanitizer/CSP/coding fix.
3. RoE for any live PoC.

### 2. Find markup injection without script

```bash
rg -n "innerHTML|dangerouslySetInnerHTML|v-html|markdown|sanitize|DOMParser" -g '*.{js,ts,tsx,jsx,vue,html}'
rg -n "ALLOWED_TAGS|addHook|dompurify|sanitize-html|bleach"
```

1. Note if `id`/`name` stripped.
2. Identify rich-text policies.

### 3. Find JS sinks that trust DOM globals

```bash
rg -n "\bdocument\.\w+\b|\bwindow\.\w+\b" -g '*.{js,ts}' | head
# Look for bare identifiers used as config in non-module scripts
```

1. Flags: `var config = ...` optional fallback to global; `document.all` legacy; feature detection via `document.x`.
2. Browser differences: clobberability varies—test target browsers.

### 4. Controlled proof (authorized)

1. Inject only named elements/forms/anchors as needed.
2. Show before/after of the trusted variable (devtools).
3. Prefer non-destructive effects (alert via existing sink, or visible config flip).
4. Multi-level form clobber → `dom-clobbering-forms`.

### 5. Severity and chaining

| Chain | Impact |
| --- | --- |
| Clobber + open redirect | Phishing |
| Clobber sanitizer options object | Bypass to XSS |
| Clobber CDN URL | Script load hijack if used as src base |
| Clobber alone | Logic bug / security feature off |

1. Score based on reachable impact, not novelty alone.

### 6. Remediation guidance

1. Use modules/bundlers—avoid bare globals for security config.
2. Namespace config: `window.__APP_CONFIG__` set as frozen object **before** untrusted HTML; or better, never on window.
3. Sanitize: strip `id`/`name` or use `DOMPurify` carefully (`dompurify-config-ops`).
4. Prefer `document.getElementById` only on trusted IDs; validate types (`instanceof` checks are subtle with elements—prefer not reading attacker-named props).
5. CSP still helps XSS; clobber is separate—fix coding patterns.

### 7. Hand off

1. Report with minimal HTML PoC + sink line numbers.
2. Regression tests: inject named tags; assert config object shape.
3. Developer education snippet in wiki.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Detection | Markup + sink review | Only script XSS scanners |
| PoC | Staging typed element | Production spam |
| Fix | No global config; sanitize names | “Users can’t put id” hope |
| Check | Explicit schema validation | `typeof === 'object'` only |
| Docs | Chain to forms skill | Ignore nested forms |
| Scope | Authorized | Random site clobber |

## Output Checklist

- [ ] Injection points for named attributes mapped
- [ ] JS sinks using document/window/bare config listed
- [ ] PoC or static proof recorded
- [ ] Browser assumptions noted
- [ ] Impact/chaining assessed
- [ ] Remediation (code + sanitizer) proposed
- [ ] Tests/guards ticketed
- [ ] Cross-link forms/XSS/DOMPurify skills
- [ ] Secrets redacted
- [ ] Residual risk noted

## Rules

- Authorized assessments only.
- Clobbering is logic/trust confusion—not always XSS.
- Prefer eliminating global config over filter whack-a-mole.
- Validate types and sources; do not trust named DOM properties as data.
- Deep form techniques in neighbor skill.
