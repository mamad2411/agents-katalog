---
name: reviewing-accessibility
description: Use this skill to review implemented UI code for WCAG accessibility compliance. Triggers when reviewing components, pages, or templates for accessibility, auditing a feature after implementation, or answering questions about accessible patterns, ARIA, keyboard navigation, or screen reader support.
compatibility: Shell access for running accessibility test commands is recommended but not required.
---

# Reviewing Accessibility

Review implemented UI code against WCAG Level AA criteria. This skill reviews code that already exists — components, pages, templates, or markup. It does not write code; findings are reported for a developer or coder agent to act on.

For pre-implementation risk assessment of plans or proposals, use `predicting-accessibility-risks` instead.

## Review process

Review the implemented code against the checklist below. Reference specific WCAG success criteria when flagging violations. Read the actual source files — do not review from memory or assumptions.

### Semantic HTML

- Correct elements used (`button`, `nav`, `main`, `article`, `h1`-`h6`, etc.)
- No `div` or `span` with `role="button"` when a native `<button>` would work
- Heading hierarchy is logical (single `h1` per page, no skipped levels)
- Lists use `ul`/`ol`/`dl` for related items, not styled divs
- Data tables have `th`, `caption` or `aria-label`

**WCAG**: 1.3.1 Info and Relationships, 2.4.6 Headings and Labels

### Keyboard navigation

- All interactive elements are keyboard accessible (Tab, Enter, Space, Escape, arrow keys as appropriate)
- Focus order follows a logical reading sequence
- No keyboard traps — every element can be navigated away from
- Skip links present for main content

**WCAG**: 2.1.1 Keyboard, 2.1.2 No Keyboard Trap, 2.4.1 Bypass Blocks

### Focus management

- Visible focus indicators on all interactive elements
- Focus trapped in modals/dialogs and returned to trigger on close
- Focus moved appropriately after dynamic content changes (creation, deletion, filtering)
- Route changes move focus to the main content area or page heading

**WCAG**: 2.4.7 Focus Visible, 2.4.11 Focus Not Obscured, 3.2.1 On Focus

### Labels and names

- All form inputs have associated `<label>` elements (not placeholder-only)
- All interactive elements have meaningful accessible names
- Images have descriptive `alt` text (or `alt=""` for decorative images)
- Error messages are programmatically associated with inputs (`aria-describedby`)
- Icon-only buttons have accessible names via `aria-label` or visually hidden text

**WCAG**: 1.1.1 Non-text Content, 1.3.1 Info and Relationships, 3.3.2 Labels or Instructions, 4.1.2 Name, Role, Value

### ARIA

- ARIA used only when native HTML cannot express the semantics
- Roles, states, and properties are valid and complete
- Live regions (`aria-live`) used for dynamic content announcements
- Loading states announced to screen readers
- `aria-current` used for navigation indicators

**WCAG**: 4.1.2 Name, Role, Value

### Visual

- Text contrast minimum 4.5:1 for normal text, 3:1 for large text
- Non-text contrast (UI components, graphical objects) minimum 3:1
- No information conveyed by colour alone
- Animations respect `prefers-reduced-motion`
- Interactive target sizes at least 24x24 CSS pixels

**WCAG**: 1.4.1 Use of Color, 1.4.3 Contrast (Minimum), 1.4.11 Non-text Contrast, 2.3.1 Three Flashes, 2.5.8 Target Size

### Forms

- Visible, persistent labels on all fields
- Required fields indicated visually and programmatically (`required` or `aria-required`)
- `aria-invalid="true"` set on fields in error state, cleared when corrected
- Error messages associated via `aria-describedby` and announced via `role="alert"` or `aria-live="assertive"`
- Appropriate `autocomplete` values on personal data fields
- Password requirements communicated before submission, not only after failure

**WCAG**: 1.3.5 Identify Input Purpose, 3.3.1 Error Identification, 3.3.2 Labels or Instructions, 3.3.3 Error Suggestion

## Report format

```markdown
## Accessibility Review - [scope description]

### Critical — WCAG Level A violations that make a feature unusable for a disability group

- **[WCAG SC]** `file:line` - [issue] -> [fix]

### Serious — WCAG Level AA violations that degrade but do not block the experience

- **[WCAG SC]** `file:line` - [issue] -> [fix]

### Moderate — Best practices and WCAG AAA improvements

- **[WCAG SC or "Best practice"]** `file:line` - [issue] -> [fix]

### Summary

[count] issues found: [n] critical, [n] serious, [n] moderate.
```

If no issues are found, say so. Do not invent findings.

## What automated tools already catch

If the project runs axe-core or a similar automated scanner, it already catches: missing alt text, duplicate IDs, basic colour contrast on static text, missing form labels, invalid ARIA attributes, missing lang attribute, landmark violations, heading level skips.

Focus review effort on what automated tools miss: dynamic state management (`aria-invalid`, `aria-expanded`, `aria-live`), focus management after interactions, keyboard trap detection, multi-theme contrast for CSS custom properties, shadow DOM internals, meaningful accessible name quality (not just presence), target size adequacy, and motion preference compliance.

Read `references/review-checklist.md` for the full prioritised checklist with WCAG criterion references.

## Gotchas

- **Working accessibility trumps theoretical compliance.** Before flagging a pattern, understand what the code does. If a component works correctly with keyboard and screen readers but uses an unconventional ARIA pattern, flag it as Moderate with an explanation of the tradeoff — not as a blocker.
- **Never recommend removing working accessibility code** without first verifying that the replacement provides equivalent or better assistive technology support.
- **Component libraries handle accessibility internally.** Many headless UI libraries (Base UI, Headless UI, Ark UI) and web component libraries (Shoelace, Web Awesome) provide built-in keyboard handling, focus trapping, and ARIA management. Adding redundant ARIA to these components can interfere with their built-in accessibility. Check the component library's documentation before recommending changes.
- **Playwright's `toHaveAccessibleName()` cannot pierce shadow DOM.** When reviewing tests for web components with shadow DOM, accessible name assertions may need to check attributes on the host element rather than using computed name matchers.
- **axe-core has known gaps.** It cannot check: CSS custom property contrast chains, shadow DOM internals, dynamic ARIA state management, focus behaviour after interactions, content behind modals or drawers, or `prefers-reduced-motion` compliance. Manual review and Playwright assertions fill these gaps.
- **Heading hierarchy is per-page, not per-component.** A component that renders an `h3` is correct or incorrect depending on the page context it appears in. Review heading levels in the context of the full page, not in isolation.
- **`aria-errormessage` has inconsistent assistive technology support.** Prefer `aria-describedby` for associating error messages with form fields — it has broader support and is functionally equivalent for this purpose.
- **Colour contrast must be checked in every theme.** A colour pairing that passes in light mode may fail in dark mode, and vice versa. Review both.

## Authoritative references

Ground all findings in the official WCAG specification and supporting documents. Do not rely on assumptions about what WCAG requires — defer to the spec:

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Understanding WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/)
- [WCAG Techniques](https://www.w3.org/WAI/WCAG22/Techniques/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria-1.2/)
- [ARIA in HTML](https://www.w3.org/TR/html-aria/)

When uncertain about a recommendation, say so explicitly and explain what could not be verified, rather than guessing.
