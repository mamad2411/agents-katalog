---
name: captcha-accessibility-balance
description: >
  Balance bot challenges with accessibility on owned apps: WCAG-aligned alternatives,
  audio/captcha issues, non-visual challenges, step-up MFA, risk-based friction, and
  support escape hatches. Use when CAPTCHA blocks screen-reader users, a11y CAPTCHA,
  accessible bot defense, or replacing visual-only challenges — not for CAPTCHA fraud.
---

# Captcha Accessibility Balance

## Scope And Authorization

- **In scope:** Applications you own; authorized UX/security design reviews.
- **Out of scope:** Bypassing third-party CAPTCHAs for abuse; disabling defenses without risk acceptance.
- Involve accessibility specialists and users of assistive tech when possible.
- Redact user support tickets’ personal data in examples.
- Pair with `captcha-enterprise-integration`, `bot-management-signals`, `accessibility-a11y-checklist`.

## When To Use

- CAPTCHA or challenge flows cause accessibility complaints or legal/WCAG risk.
- Designing risk-based friction that still works with screen readers, keyboard-only, cognitive disabilities.
- Replacing pure visual puzzles with better alternatives (passkeys, email/SMS OTP carefully, vendor a11y modes).
- Auditing third-party CAPTCHA widgets for a11y failures on your pages.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Enterprise CAPTCHA install | `captcha-enterprise-integration` |
| Authorized control effectiveness testing | `captcha-bypass-research` |
| Bot signal architecture | `bot-management-signals` / fusion |
| General WCAG site audit | `accessibility-a11y-checklist` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Tension | Direction |
| --- | --- |
| Bot friction vs inclusion | Prefer invisible/risk-based; challenge only when risk high |
| Visual puzzles | Often fail WCAG; need alternatives |
| Audio CAPTCHA | Frequently still unusable; do not rely alone |
| Time limits | Cognitive load; allow extend/retry without trap |
| Support | Human review path with fraud controls |

## Workflow

### 1. Confirm scope and success criteria

1. Surfaces using challenges (login, signup, checkout, comments).
2. Success: documented accessible path for each surface; measured challenge pass rates by AT user cohort if available; legal/a11y review notes.
3. Risk owners accept residual bot risk for softer paths.

### 2. Inventory current challenges

```bash
# Find CAPTCHA widgets in owned frontends
rg -n "recaptcha|hcaptcha|turnstile|captcha|challenge" -g '*.{js,ts,tsx,html,vue}'
```

1. For each: vendor, visual-only?, keyboard operable?, screen reader labels, timeout, mobile.
2. Collect support tickets tagged accessibility + CAPTCHA.
3. Note localization (audio language coverage).

### 3. Assess against a11y criteria

| Check | Pass example |
| --- | --- |
| Keyboard | Complete challenge without mouse |
| Screen reader | Name/role/value announced; focus order logical |
| Contrast | Puzzle UI meets contrast (if visual) |
| Time | User can extend; no silent expire mid-AT |
| Alternative | Non-visual path available and discoverable |
| Cognitive | Instructions plain language; not only abstract images |
| Error | Clear recovery, not “try again” loop only |

1. Manual AT test: NVDA/JAWS/VoiceOver on staging.
2. Automated a11y scans catch markup issues but **not** puzzle solvability — still need human AT test.

### 4. Design balanced policy

**Preferred hierarchy:**

1. **Reduce challenge frequency** via better bot signals (server-side) so most humans never see CAPTCHA.
2. **Invisible / low-friction** vendor modes when risk low.
3. **Accessible step-up**: passkey, WebAuthn, TOTP, email magic link (with rate limits), known-device cookie.
4. **Vendor accessible challenge** with tested AT support — verify, don’t assume.
5. **Human support escalation** for locked-out users (identity verification playbook).

**Avoid as sole path:**

- Image grids with no AT alternative.
- Audio CAPTCHA only.
- Challenges that break in high-contrast / zoom 200%.

```text
# Policy sketch
if risk == low: allow
elif risk == medium and user.has_webauthn: step_up_webauthn
elif risk == medium: vendor_challenge_a11y_mode
elif risk == high: hard challenge + rate limit + optional manual review queue
```

### 5. Implement integration requirements

1. Challenge iframe/widget must not trap focus permanently.
2. Announce dynamic errors via `aria-live`.
3. Ensure server-side verification still authoritative (`captcha-enterprise-integration`).
4. Provide visible link: “Need another way to verify?” → alternate method.
5. Logging: challenge type used, success/fail — **not** disability status inference beyond voluntary feedback.

### 6. Verify

1. Keyboard-only signup/login journeys on staging.
2. Screen reader walkthrough recorded (internal).
3. Mobile VoiceOver/TalkBack.
4. Bot risk: ensure alternate path is not a free automation oracle (rate limit, device binding, velocity).
5. Load test alternate OTP paths for abuse (`rate-limit-bypass-testing` authorized).

### 7. Hand off

1. Publish a11y + bot defense decision record.
2. Support runbook for manual verification with fraud checks.
3. Monitor challenge abandon rates and a11y tickets.
4. Apply `code-quality-standards` and general a11y checklist to surrounding pages.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default UX | Most users never challenged | CAPTCHA every page load |
| Alternative | Passkey / tested vendor a11y | Audio-only afterthought |
| Focus | Manageable widget focus | Keyboard trap in iframe |
| Abuse | Rate-limited alts | Email OTP unlimited = bot signup |
| Process | AT user testing | “Lighthouse 100 = fine” |
| Support | Documented human path | “Reset CAPTCHA” only reply |

## Output Checklist

- [ ] Challenge surfaces inventoried
- [ ] AT/keyboard assessment done
- [ ] Risk-based challenge frequency reduced where possible
- [ ] Accessible alternatives implemented and linked
- [ ] Server verification + abuse controls on alts
- [ ] Support escalation runbook
- [ ] Metrics for abandon/fail by challenge type
- [ ] Legal/a11y stakeholder sign-off as required
- [ ] `code-quality-standards` / a11y checklist applied

## Rules

- Accessibility is not optional “nice to have” on auth surfaces — design dual goals.
- Alternatives must not nullify bot defense.
- Test with real assistive technology, not only scanners.
- Authorized product changes only.
- Control-bypass research stays in `captcha-bypass-research` under RoE.
