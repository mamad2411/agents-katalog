---
name: dsn-accessibility-review
version: 1.0.0
description: Audit a screen, flow, or component against WCAG 2.1 AA - contrast, keyboard operability, target sizes, and screen-reader semantics - and return prioritized, fixable findings with cited success criteria.
author: matrixx0070
tags: [design, accessibility, wcag, audit, a11y, screen-reader]
capabilities: []
---

# Accessibility Review

## When to use
Use this before shipping any UI, when a design or build must clear WCAG 2.1 AA, or when someone reports a control that is unreachable, illegible, or invisible to assistive tech. Works on mockups, live pages, or component specs.

**Not for:** full manual AT test passes with real users (this is an expert heuristic audit), legal certification/VPAT authoring, or general design taste — for that use dsn-design-critique.

## Method
1. **Scope the surface.** Enumerate every interactive element, text block, image, and state (hover, focus, error, disabled, loading, empty). You cannot audit what you have not listed.
2. **Contrast.** Measure text against its *actual* background: 4.5:1 body, 3:1 large text (>=24px or >=19px bold) and UI/graphical boundaries. Report measured ratios, never "looks fine". *Decision:* if a ratio is between 4.4 and 4.5, treat as fail and give the nearest passing value.
3. **Keyboard.** Trace Tab order; confirm every action is reachable, focus is always visible, order matches visual flow, no traps. *Decision:* if a custom widget (menu, tabs, modal) exists, verify the expected Esc/Enter/arrow keys per ARIA Authoring Practices — flag if unclear.
4. **Targets and spacing.** Flag touch targets under 44x44px and adjacent targets with no gap.
5. **Screen-reader semantics.** Verify name/role/state: alt text, labels tied to inputs, heading hierarchy, landmarks, aria-live for dynamic content, error text linked to its field.
6. **Prioritize.** Sort blocker (locks a user out) > serious > minor. *Decision:* when unsure of severity, ask "can the user complete the task at all?" — if no, it is a blocker.

## Example
A "Delete account" button is `#9AA0A6` text on `#FFFFFF` (2.9:1) and only reachable by mouse. Findings: **Blocker** — 2.1.1 Keyboard: button not focusable, add to tab order; **Serious** — 1.4.3 Contrast: 2.9:1 fails 4.5:1, darken to `#5F6368` (7.0:1).

## Pitfalls
- Auditing the mockup's happy path only — error, empty, and loading states ship broken most often.
- Reporting "low contrast" without the measured ratio and a passing replacement color.
- Trusting a color-contrast plugin on gradient or image backgrounds; sample the worst-case pixel.
- Confusing "focusable" with "operable" — an element can receive focus yet do nothing on Enter/Space.

## Output format
```
# A11y Audit: <surface> (WCAG 2.1 AA)
**Blockers:** <criterion X.X.X> — issue — one-line fix
**Serious:** <criterion> — issue — fix
**Minor:** <criterion> — issue — fix
**Passed:** <what already conforms>
```
Cite the specific success criterion (e.g. 1.4.3 Contrast) and give a concrete, one-line fix per finding.

## Reference

### Highest-frequency real-world failures (check these first)
1. Inputs with no programmatic label (placeholder ≠ label) — 3.3.2 / 1.3.1.
2. Focus not visible or removed via `outline:none` — 2.4.7.
3. Error announced but **focus not moved** to it — user stranded (see below).
4. Contrast < 4.5:1 on body text / < 3:1 on UI borders — 1.4.3 / 1.4.11.
5. Custom widget (dropdown, tabs, modal) missing keyboard + ARIA — 4.1.2.

### Focus management (the #1 multi-step-form dead-end) — 2.4.3
On a failed submit, move focus to the **first invalid field or an error summary** (`tabindex="-1"` + focus); don't just add `role="alert"`. On a step change, move focus to the new step's heading and update the page `<title>` (2.4.2). Announcing an error without moving focus leaves screen-reader users lost.

### Form grouping & semantics
- Wrap related radios/checkboxes (shipping method, card type) in `<fieldset>` + `<legend>` — 1.3.1.
- Set `aria-invalid="true"` on failed fields and tie the message via `aria-describedby`.
- **Label-in-name (2.5.3):** the accessible name must contain the visible label text so voice-control users can say "click Pay now".
- **Use of color (1.4.1):** a red border alone can't signal an error — pair with text/icon.
- Accessible step indicator: mark the current step with `aria-current="step"`.

### Checkout / payment specifics
- **CAPTCHA (1.1.1):** any image CAPTCHA at payment is a purchase blocker — require an accessible alternative (audio/token).
- Third-party payment **iframes** (Stripe/Braintree) must be in the tab order and labeled.
- Card fields that **auto-advance** must not steal focus mid-correction; inputs must accept pasted formatted numbers.
- Session timeouts (2.2.1) need a warning + extend option; don't wipe entered data.

### Test matrix (rough time per check)
Keyboard-only pass (~10 min) · screen reader NVDA/VoiceOver (~20 min) · 200% zoom + 320px reflow 1.4.10 (~5 min) · contrast sample (~10 min) · forms/error flow (~15 min).
