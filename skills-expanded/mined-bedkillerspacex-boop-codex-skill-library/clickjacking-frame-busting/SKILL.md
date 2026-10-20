---
name: clickjacking-frame-busting
description: >
  Frame-busting scripts and their limits: top.location tricks, sandbox bypasses, and
  why CSP frame-ancestors / X-Frame-Options must be primary. Use when reviewing legacy
  JS anti-framing, migrating off busting scripts, or explaining residual risk — not as
  the sole clickjacking defense for new systems (use clickjacking + defense-checklist).
---

# Clickjacking Frame-Busting

## Scope And Authorization

- **In scope:** owned apps and authorized code review of anti-framing measures.
- **Out of scope:** developing better ways to bypass third-party protections without auth.
- Treat frame-busters as **legacy depth**, never the only control.
- Pair migrations with `clickjacking-defense-checklist` and CSP skills.

## When To Use

- Codebase contains `if (top !== self) top.location = ...` style scripts.
- Stakeholder asks “we have frame-busting JS — enough?”
- Sandbox attribute or design issues make busting fail.
- Tokens: frame-busting, top.location, sandbox, ancestorOrigins, legacy anti-frame.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Assessment / PoC | `clickjacking` |
| Org rollout of headers | `clickjacking-defense-checklist` |
| Advanced redress research | `clickjacking-ui-redress-deep` |
| Full CSP | `content-security-policy-design` |

## Why JS Busting Is Insufficient

| Limitation | Detail |
| --- | --- |
| Sandbox | `iframe sandbox` without `allow-top-navigation` can block busting |
| Race | User may click before script runs |
| UX fail-open | Errors / CSP blocking inline script disable buster |
| Maintenance | Easy to drop on new SPA shells |
| Double-frame / filter tricks | Historical bypass literature |

**Primary controls remain:** CSP `frame-ancestors` and `X-Frame-Options`.

## Workflow

### 1. Inventory busting code

```bash
rg -n "top\.location|top\.location\.href|parent\.location|frameElement|ancestorOrigins" --type js --type ts
rg -n "X-Frame-Options|frame-ancestors"
```

1. Note where script is injected (layout, GTM, only some routes).
2. Check CSP: does it allow the buster script?

### 2. Classify current protection

| State | Risk |
| --- | --- |
| Headers strong + JS buster | OK depth; buster optional |
| JS only | High residual risk |
| Neither | Critical for sensitive UI |
| Headers only | Preferred modern baseline |

### 3. Understand common patterns (legacy)

```javascript
// Classic (incomplete alone)
if (window.top !== window.self) {
  window.top.location = window.self.location;
}

// "Stop loading" variants (still not primary defense)
```

1. Document intended behavior for legitimate same-site frames.
2. Identify breakages: payment iframes, chat widgets, design systems.

### 4. Migration plan

1. Deploy CSP `frame-ancestors` (+ XFO) per `clickjacking-defense-checklist`.
2. Verify hostile iframe blocked **without** JS.
3. Remove or slim buster after header coverage proven (optional keep as rare legacy UA depth).
4. If legitimate framing required, allowlist origins in CSP — do not disable headers globally.

### 5. If temporarily stuck with JS only (lab/legacy)

1. Ticket the residual risk; time-box.
2. Ensure script is early, non-blocked by CSP, not only on marketing pages.
3. Still add server headers ASAP.
4. Do not claim PCI/high-assurance compliance on busting alone.

### 6. Verify

```bash
curl -sI https://app.example.com/ | rg -i "frame-ancestors|x-frame-options"
# Browser tests:
# 1) evil iframe with sandbox lacking allow-top-navigation → buster fails; headers must save you
# 2) after CSP: iframe blank/blocked even if buster removed
```

### 7. Hand off

1. Code review comment template: “Replace frame-buster reliance with frame-ancestors”.
2. Link PR that adds headers and optionally deletes obsolete JS.
3. Record any partner embed allowlist.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Primary defense | CSP frame-ancestors | Busting script only |
| Sandbox awareness | Tested | Ignored |
| Migration | Headers first, then delete JS | “New buster version” forever |
| Evidence | Header + sandbox PoC | “Script looks present” |
| Legit embeds | CSP allowlist | `if (false)` disable buster for all |

## Output Checklist

- [ ] Frame-buster call sites inventoried
- [ ] Header posture recorded
- [ ] Residual bypass paths documented (sandbox/race)
- [ ] Migration to frame-ancestors planned or done
- [ ] Verification without relying on JS
- [ ] Stakeholders informed busting ≠ complete fix
- [ ] Optional JS removal after headers proven

## Rules

- Never present frame-busting as sufficient sole control for new work.
- Authorized review only when testing bypasses.
- Prefer reversible header rollout with embed regression tests.
- Keep this skill focused on **busting limits and migration**; primary offense/defense skills are siblings.
