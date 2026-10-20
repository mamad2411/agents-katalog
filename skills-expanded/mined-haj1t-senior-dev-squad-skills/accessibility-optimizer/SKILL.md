---
name: accessibility-optimizer
description: "WCAG 2.2 AA/AAA auditing, automated fixing, UI accessibility quality gate. Use when auditing or fixing UI accessibility issues."
---

# Accessibility Optimizer

## Overview

Accessibility Optimizer audits and automatically corrects all generated UIs to comply with WCAG 2.2 AA/AAA standards. It systematically verifies four core principles: Perceivable, Operable, Understandable, and Robust. It covers dimensions ranging from color contrast and keyboard navigation to screen reader compatibility and cognitive accessibility.

**Core principle:** Accessibility is not a feature; it is a quality requirement. No UI can be published without passing accessibility auditing.

## The Iron Law

```
NO UI CAN BE PUBLISHED WITHOUT PASSING A WCAG 2.2 AA (AT MINIMUM) AUDIT. COLOR CONTRAST, KEYBOARD NAVIGATION, AND SCREEN READER SUPPORT ARE ABSOLUTE MUST-HAVE REQUIREMENTS.
```

## When to Use

**Use this when:**
- Every time a new UI component or page is generated.
- Changes are made to an existing UI.
- The client requests an accessibility certificate.
- Color palettes or typography change.
- User feedback reports accessibility issues.

**Use this ESPECIALLY when:**
- Legal requirements apply (public sites, e-commerce, banking).
- The release date is close and there is pressure to "handle it later."
- A global/multilingual product is being developed.

**Don't skip when:**
- Never (accessibility is mandatory for all UIs).

## Workflow

Work through all nine phases in order. Each gate must be confirmed before proceeding.

**Phase 1 — WCAG 2.2 Auditing (Four Principles Scan).** Audit Perceivable, Operable, Understandable, and Robust compliance. See [REFERENCE.md](REFERENCE.md) for the full checklist per principle and a robust HTML structure example.

**Phase 2 — Color Contrast Audit.** Test all text/background pairs against AA (4.5:1 normal, 3:1 large) and AAA (7:1 normal, 4.5:1 large) targets; verify focus-ring and non-text contrast (3:1). See [REFERENCE.md](REFERENCE.md) for the contrast calculation function and recommended color fixes.

**Phase 3 — Keyboard Navigation Audit.** Verify tab order, visible focus indicators, skip links, focus-trap behavior in modals, and custom shortcut disableability. See [REFERENCE.md](REFERENCE.md) for skip-link, focus-style, and focus-trap code patterns.

**Phase 4 — Screen Reader Audit.** Verify ARIA labels/roles, live regions, alt text, heading hierarchy (h1→h2→h3), and form labels. See [REFERENCE.md](REFERENCE.md) for ARIA button and live-region markup examples.

**Phase 5 — Form Accessibility Audit.** Confirm every input has a `<label>`, errors are bound via `aria-describedby`, required fields are marked, error announcements fire on submit, and `autocomplete` is set. See [REFERENCE.md](REFERENCE.md) for a complete accessible form structure example.

**Phase 6 — Motion Sensitivity.** Apply `prefers-reduced-motion` to disable or minimize all animations, parallax, autoplay, and flashing content (WCAG 2.3.1). See [REFERENCE.md](REFERENCE.md) for the CSS media query block and `.animations-disabled` class.

**Phase 7 — Cognitive Accessibility.** Ensure clear language, consistent navigation, error prevention/undo for critical actions, session-timeout warnings, help guidance for complex flows, and visual consistency. See [REFERENCE.md](REFERENCE.md) for a step-indicator progressbar markup example.

**Phase 8 — Automated Fixing (Auto-Fix).** Categorize issues (Critical/Medium/Improvement), generate corrected HTML/CSS/JS, add missing ARIA, fix color values, correct structural HTML, and produce a change log. See [REFERENCE.md](REFERENCE.md) for diff examples of form and color auto-fixes.

**Phase 9 — Final Verification (Quality Gate).** Run the checklist below. See [REFERENCE.md](REFERENCE.md) for the prose self-review questions and legal compliance notes.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:

- "There are no visually impaired users on this page, we can handle accessibility later" — Accessibility is for all users, not just those with impairments.
- "We only check color contrast with a tool, no manual test needed" — Tools cannot find all issues. Manual testing is mandatory.
- "ARIA solves everything, no need for semantic HTML" — ARIA does not replace semantic HTML; it only supplements it.
- "Keyboard navigation is only for developers" — It is vital for keyboard users (those with motor or visual impairments).
- "prefers-reduced-motion is only for a small group" — Animations can cause physical discomfort for users with vestibular disorders.
- "AAA level is too hard, AA is enough" — AA is the mandatory minimum. Aim for AAA whenever possible.

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Accessibility can be added later, functionality first" | Accessibility cannot be bolted on; it must be built into the foundation. Retrofitting is 3-5x more expensive. |
| "Colorblind users are very rare" | There are ~300 million colorblind users worldwide. Contrast also improves readability for everyone. |
| "Let's use ARIA everywhere to solve the issue" | Poor ARIA is worse than no ARIA. ARIA should only be used when proper semantic HTML is not possible. |
| "Keyboard testing takes too much time" | It takes 10 minutes with automated tools + a quick manual check, and is vital for keyboard users. |
| "It looks beautiful visually, accessibility will ruin it" | Accessibility and beautiful design are not mutually exclusive. Both are possible. |
| "If users use assistive technology, it's their responsibility, not ours" | WCAG is a legal standard. Ethically, we must build products for everyone. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**

- "It's not clear what this button does" — Missing ARIA label or visual text.
- "The screen reader skipped this section" — Missing semantic HTML or ARIA role.
- "Cannot exit this dialog box using a keyboard" — Focus trap is incorrectly configured.
- "These colors look very washed out on mobile" — Contrast ratio gets worse on mobile displays.
- "Nothing happened after submitting the form" — Error messages are not announced to the screen reader.
- "This animation is making my head spin" — prefers-reduced-motion is not supported.
- "Buttons overflow when zoomed in" — Responsive + accessibility were not tested together.

**When you see these:** STOP. Return to the relevant phase.

## Related Skills

- **responsive-layout-engine** — Should be run after layout design to verify responsive layout accessibility.
- **component-library-generator** — Generates accessible versions of all components (including ARIA).
- **design-system-extractor** — Used before accessibility auditing to check contrast rules of color tokens.
- **performance-auditor** — Used to evaluate the performance impact of accessibility fixes (extra DOM, ARIA attributes).
- **color-theory-engine** — Used during color palette generation to produce colors complying with contrast rules.

## Verification

Final checklist before marking complete:

- [ ] All WCAG 2.2 AA criteria are met.
- [ ] Color contrast is at least 4.5:1 for normal text.
- [ ] Color contrast is at least 3:1 for large text.
- [ ] All interactive elements are keyboard-accessible.
- [ ] Skip link is present and functional.
- [ ] All images have meaningful alt text (decorative images have `alt=""`).
- [ ] Heading hierarchy (h1 → h2 → h3) is correct.
- [ ] All form elements are labeled.
- [ ] Error messages are announced by screen readers.
- [ ] `prefers-reduced-motion` is supported.
- [ ] Page language tag (`lang`) is correct.
- [ ] ARIA usage complies with standards and is meaningful.
- [ ] Automated fix report is generated and applied.
- [ ] Manual testing has been performed with at least one screen reader (VoiceOver/NVDA/JAWS).
- [ ] Page remains usable at 200% zoom.
