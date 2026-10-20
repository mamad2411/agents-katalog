---
name: dom-clobbering-forms
description: >
  DOM clobbering via forms, inputs, and anchors: multi-level property chains
  (form.element.value), collection behaviors, and hardening for owned apps that render
  attacker-influenced HTML. Use when form/input name clobbering, document.forms tricks,
  anchor id clobber, or nested DOM clobber against JS config checks during authorized
  reviews — pair awareness skill for general patterns and DOMPurify for sanitizer ops.
---

# DOM Clobbering Forms

## Scope And Authorization

- **In scope:** Owned web apps and authorized assessments.
- **Out of scope:** Drive-by exploitation of third parties without RoE.
- Prefer staging PoCs; keep payloads minimal.
- Pair with `dom-clobbering-awareness`, `dompurify-config-ops`, `xss-cross-site-scripting`, and `code-quality-standards`.

## When To Use

- Filters allow `<form>`, `<input>`, `<a>`, `<img>`, `<button>` with `name`/`id`.
- JS checks like `config.isAdmin.value` or nested property walks.
- Sanitizer leaves forms but strips scripts—false sense of safety.
- Reviewing client-side feature flags read from DOM-ish objects.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General clobber awareness | `dom-clobbering-awareness` |
| Classic XSS | `xss-cross-site-scripting` |
| DOMPurify configuration | `dompurify-config-ops` |
| CSRF on forms | framework CSRF skills |
| Code quality baseline | `code-quality-standards` |

## Why forms matter

HTML forms and named controls create **nested** structures reachable as properties. Attackers may craft markup so that expressions intended for plain objects resolve to DOM nodes with useful `.value`, `.href`, or further named children—passing shallow truthy/object checks.

```html
<!-- Illustrative multi-level style markup (browser-dependent) -->
<form id="config">
  <input name="isAdmin" value="true" />
</form>
```

```javascript
// Dangerous: treating clobbered structure as data
if (config.isAdmin) {
  enableAdminUi();
}
// Or reading .value believing it's your settings object field
```

| Element | Common clobber surface |
| --- | --- |
| `<a id="x" href="...">` | `x` global; `.href` string coercion |
| `<form id="x">` | Container for named controls |
| `<input name="y">` | Nested `x.y` style access patterns |
| Multiple same names | RadioNodeList / collections |

## Workflow

### 1. Confirm scope and success criteria

1. HTML sinks and sanitizer allowlists for form-related tags.
2. Success: forms/inputs/anchors cannot rewrite security decisions; tests cover nested names.
3. Authorized PoC only.

### 2. Inspect sanitizer allowlists

```bash
rg -n "FORM|INPUT|A |BUTTON|name|ADD_ATTR|ALLOWED_TAGS" -g '*.{js,ts,py,go}'
```

1. If `FORM`/`INPUT` allowed in UGC, escalate review priority.
2. Check whether `name` and `id` attributes permitted.

### 3. Find nested property reads in JS

```bash
rg -n "\\.value\\b|featureFlags|isAdmin|getAttribute\\('value'\\)" -g '*.{js,ts,tsx}'
```

1. Trace origins of objects used in security decisions—built-in JSON only?
2. Flag code that does `obj.a.b` after optional untrusted HTML parse in same document.

### 4. Authorized proof methodology

1. Start with single-level id clobber (`dom-clobbering-awareness`).
2. Escalate to form/input nesting only if shallow checks still pass for the sink.
3. Record browser version—behavior differs.
4. Prefer proving config corruption over chaining to high-impact exploits when code review suffices.

### 5. Hardening

| Control | Practice |
| --- | --- |
| Sanitize | Disallow `form`/`input` in UGC; strip `id`/`name` if tags needed |
| DOMPurify | Tight `ALLOWED_TAGS` / `ALLOWED_ATTR`; hooks to remove names |
| Code | Config from JSON module scope; `Object.freeze`; never globals |
| Checks | Prefer explicit maps (`settings.isAdmin === true` from server) |
| iframe sandbox | Untrusted HTML in sandboxed iframe with null origin when possible |
| CSP | Helps script XSS; still fix clobber sources |

```javascript
// Safer pattern
import { settings } from "./settings.js"; // not from DOM
if (settings.isAdmin === true) {
  enableAdminUi();
}
```

### 6. Tests

```html
<!-- fixtures/ugc_clobber.html -->
<form id="config"><input name="isAdmin" value="true" /></form>
```

1. After render, assert `settings` object unchanged and not an `HTMLElement`.
2. Snapshot sanitizer output without name/id where policy forbids.

### 7. Hand off

1. Report allowlist + sink + minimal form markup.
2. Ticket sanitizer change and JS global removal.
3. Retest after DOMPurify config update.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| UGC policy | No form/input in comments | Allow all non-script tags |
| Config | Bundled JS module | `window.config` after HTML |
| PoC | Minimal form/input | Huge gadget pages |
| Fix | Strip name/id + no globals | Block only `<script>` |
| Test | Fixture asserts types | Manual only once |
| Scope | Authorized | Third-party drive-by |

## Output Checklist

- [ ] Form-related tags in sanitizer reviewed
- [ ] Nested JS property sinks listed
- [ ] Browser-tested PoC or static proof
- [ ] Hardening: sanitizer + code pattern
- [ ] Server-driven authZ for admin features
- [ ] Regression fixtures added
- [ ] iframe isolation considered for UGC
- [ ] Cross-links to awareness/DOMPurify
- [ ] Residual risk documented
- [ ] `code-quality-standards` on fixes

## Rules

- Forms/inputs are high-value clobber primitives when allowed in HTML.
- Security decisions must not read attacker-named DOM properties.
- Authorized testing only; minimal payloads.
- Coordinate with general awareness and sanitizer skills.
- AuthZ always enforced server-side—client clobber must not grant privilege alone if server is correct (still fix client).
