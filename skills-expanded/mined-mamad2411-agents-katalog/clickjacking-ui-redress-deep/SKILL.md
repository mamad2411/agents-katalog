---
name: clickjacking-ui-redress-deep
description: >
  Deep UI redress analysis beyond basic iframes: multi-step clickjacking, partial
  overlays, drag-and-drop redress, cursor/focus tricks, popup/tab under, and
  mobile touch redress — for authorized assessments and robust defense design.
  Use when basic XFO/CSP review is insufficient or high-value actions need threat
  modeling; primary simple cases stay in clickjacking.
---

# Clickjacking UI Redress (Deep)

## Scope And Authorization

- **In scope:** owned apps, labs, authorized red-team/purple-team web assessments.
- **Out of scope:** weaponizing redress against third parties or real users without ROE.
- Prefer synthetic accounts; no production fund movement.
- Document PoCs carefully; redact cookies.
- Pair with `clickjacking` and `clickjacking-defense-checklist`.

## When To Use

- Target already has partial framing protections or complex SPA UX.
- Evaluating **defense-in-depth** for banking/admin/OAuth consent UIs.
- Researching residual risk after `frame-ancestors 'none'`.
- Tokens: UI redress, cursorjacking, drag-drop jacking, strokejacking, nested frames, mobile redress.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Standard clickjacking test/fix | `clickjacking` / `clickjacking-defense-checklist` |
| Frame-buster migration | `clickjacking-frame-busting` |
| XSS | `xss-cross-site-scripting` |
| CSRF-only | CSRF skill / cookie SameSite skills |
| CSP whole-policy design | `content-security-policy-design` |

## Technique Catalog (authorized lab)

| Technique | Idea | Mitigations beyond headers |
| --- | --- | --- |
| Basic overlay | Transparent iframe over decoy button | frame-ancestors, XFO |
| Multi-step | Sequence of framed clicks (wizard) | Step-up auth, short-lived intent tokens |
| Partial expose | Only “Confirm” peeks through mask | Avoid one-click high impact; confirm text must be victim-controlled not attacker |
| Nested frames | Extra frame layers / filters | CSP ancestors; simplify embed model |
| Cursor offset | Custom cursor misalignment | pointer-events hardening; avoid critical hit targets near edges only |
| Drag-and-drop | Victim drags attacker content into framed field | Disable dangerous drop targets; sanitize |
| File upload jack | Overlay upload control | Re-auth; confirm filename server-side UX |
| Popup under / focus steal | Timing with windows | COOP/focus UX; avoid auto privilege |
| Mobile touch | Touch target mismatch | Larger confirms; no invisible layers on sensitive apps |
| XSS-assisted | Inject overlay in-origin | Fix XSS first |

**Note:** Strong `frame-ancestors 'none'` blocks cross-origin iframe load of victim UI — many pure framing techniques die there. Deep work then focuses on **same-origin** assist (XSS), **legitimate embed** abuse, or non-frame redress (phishing UX), which may route to other skills.

## Workflow

### 1. Threat model the critical journeys

1. List top 5 state-changing journeys (consent, pay, role grant, disable security).
2. For each: clicks required, CSRF posture, frame policy, step-up auth, mobile variants.
3. Mark journeys that **must** be embeddable (if any).

### 2. Establish baseline controls

```bash
curl -sI "$URL" | rg -i "frame-ancestors|x-frame-options|content-security-policy"
```

1. If framing open → start with `clickjacking` PoC, then escalate multi-step.
2. If framing closed → document residual non-frame risks; do not invent unauthorized XSS.

### 3. Authorized deep PoC design

1. Build attacker page only on lab domain.
2. Prototype multi-step: decoy game / CAPTCHA-like sequence aligning clicks to victim controls.
3. Measure success rate with **test accounts** only; record video for report.
4. Test mobile viewports and pointer/touch separately.
5. Test whether **allowed** partner embed origin can be combined with open redirect/XSS (chain).

### 4. Defense recommendations (high assurance)

| Control | Purpose |
| --- | --- |
| `frame-ancestors 'none'` or strict list | Kill cross-origin frames |
| XFO DENY/SAMEORIGIN | Legacy depth |
| CSRF + SameSite=Lax/Strict | Block simple cross-site POST |
| Step-up / WebAuthn for sensitive ops | Click ≠ authority |
| Transaction confirmation text server-bound | User sees real amount/role |
| Short-lived action tokens | Multi-step expires |
| Separate embeddable widget origin | Minimize privileged surface |
| COOP/COEP where isolation needed | See coop-coep skills |
| No sensitive action on first paint without gesture semantics that are clear | UX |

### 5. Verify defenses

1. Cross-origin iframe: blocked.
2. Multi-step PoC fails when step-up or action token required.
3. Partner allowlist cannot reach admin routes (path-separated).
4. Automated regression for headers + critical journey step-up flags.

### 6. Report structure

1. Technique attempted, prerequisites, success/fail, CVSS-like narrative impact.
2. Separated: pure clickjacking vs chained (XSS/CSRF).
3. Fix verification steps for engineering.

### 7. Hand off

1. Engineering implements checklist skill items.
2. Residual accepted risks signed by owner (e.g. required third-party frame).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | ROE + test accounts | Real customer phishing |
| Depth | Multi-step with evidence | Claim “undetectable 0day” without PoC |
| Defense | Headers + step-up | Only CSS `pointer-events` games |
| Framing closed | Pivot to real residual risks | Pretend iframe still loads |
| Chains | Document XSS dependency | Bundle unrelated bugs |

## Output Checklist

- [ ] Critical journeys threat-modeled
- [ ] Baseline frame headers recorded
- [ ] Deep techniques attempted only in scope
- [ ] Evidence (pass/fail) per technique
- [ ] High-assurance controls recommended/implemented
- [ ] Verification of step-up / tokens where required
- [ ] Clear report with non-frame residuals
- [ ] Owners accepted residual embed risks

## Rules

- Authorized deep testing only; no real-user harm.
- Prefer reproducible lab PoCs over theoretical essays alone.
- Do not skip basic `frame-ancestors` for exotic mitigations.
- Focus on **advanced redress**; simple cases and rollout stay in sibling skills.
