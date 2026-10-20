---
name: common-a11y
description: Accessibility (WCAG 2.2 AA+, ARIA, assistive-tech compatibility, keyboard / switch / voice / screen-reader UX). Auto-invoked when building UI, prepping for audit, or remediating a11y findings.
---

# Accessibility

Accessibility is the standard that stress-tests the rest of your UX: a keyboard-only
user, a screen-reader user, and a low-vision user each find the bugs sighted
mouse-using users never will.

## When to reach for this

- Building or reviewing UI components for WCAG 2.2 AA conformance
- Preparing for an accessibility audit, or producing an ACR/VPAT
- Remediating findings — prioritizing by user impact, fixing at the component level
- Designing keyboard behavior, focus management, or screen-reader announcements

## Principles

1. **HTML first, ARIA second.** `<button>` beats `<div role="button" tabindex="0">`
   every time. ARIA fills gaps in HTML semantics — most a11y bugs are ARIA used where
   plain HTML was sufficient.
2. **Test with a screen reader, not just a checker.** Automated tools like axe catch
   roughly 30% of issues. The rest — nonsense announcements, misplaced focus, lost
   context — are only findable by actually using NVDA or VoiceOver.
3. **Keyboard is the baseline.** Every interactive element reachable with Tab,
   operable with Enter/Space, escapable with Esc. Focus never gets trapped behind a
   hidden element or dropped to `<body>`.
4. **Motion and contrast are settings-aware.** Respect `prefers-reduced-motion` and
   `prefers-contrast`; test Windows high-contrast mode. Contrast minimums: 4.5:1 for
   body text, 3:1 for large text and UI components. Never convey state or error by
   color alone.
5. **Fix at the component, not the page.** Accessibility lives in the design system —
   if `<Button>` is right, every page is right. One-off page fixes don't scale.
6. **Publish an honest ACR.** A conformance report with truthful partial-support
   disclosures beats a perfect-looking lie; procurement teams check.

## Screen-reader test matrix

| Combination | Platform | Covers |
|---|---|---|
| NVDA + Chrome | Windows | most common free pairing |
| JAWS + Chrome | Windows | enterprise / procurement baseline |
| VoiceOver + Safari | macOS | the only supported macOS pairing |
| VoiceOver + Safari | iOS | mobile web |
| TalkBack + Chrome | Android | mobile web |

For each flow, verify announcement *quality* — name, role, value, state changes via
`aria-live` — not just that something is read.

## Component a11y spec (per interactive component)

- [ ] Role: native element or explicit ARIA role
- [ ] Keyboard: Tab order, activation keys (Enter/Space), Esc behavior, arrow-key
      pattern for composite widgets (per the ARIA Authoring Practices)
- [ ] Labels: accessible name, `aria-describedby` for hints, error association on inputs
- [ ] Focus: visible indicator, programmatic focus on open/close, no traps
- [ ] Announcement: what a screen reader says on reach, activation, and state change
- [ ] Tests: automated (axe) + a written manual screen-reader script

## Pitfalls

- `aria-label` on a `<div>` with a click handler instead of a real `<button>`
- Focus left on a removed element after a modal closes (lands on `<body>`)
- `aria-live` regions added after page load, or spamming announcements on every keystroke
- Placeholder text doing the job of a `<label>`
- Custom dropdowns/comboboxes that ignore the expected arrow-key and type-ahead behavior
- Auto-playing motion with no pause and no `prefers-reduced-motion` fallback
- An ACR that claims "Supports" for criteria nobody manually tested

---
*Related: `ux-design` (overall usability critique), `common-i18n` (RTL interacts with
focus order), `common-notifications` (accessible email/in-app templates) · pulled by
any domain agent · output/ADR format: `playbook-conventions`*
