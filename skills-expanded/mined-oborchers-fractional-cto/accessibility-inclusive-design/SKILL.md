---
name: accessibility-inclusive-design
description: This skill should be used when the user is implementing accessible design, checking color contrast ratios, adding keyboard navigation, supporting screen readers, handling color blindness, implementing ARIA attributes, designing focus indicators, meeting WCAG 2.2 compliance, or building inclusive interfaces. Covers WCAG 2.2 AA requirements, color contrast (4.5:1 body, 3:1 large text), color independence (never rely on color alone), keyboard navigation, focus indicators, touch targets, screen reader considerations, and automated testing with axe-core.
version: 1.0.0
---

# Accessibility Is Not a Feature -- It Is a Design Quality Indicator

16% of the global population has a disability (WHO). Accessibility is not an edge case -- it is a core design quality dimension. WCAG 2.2 AA compliance is the minimum bar, not a stretch goal. Inaccessible design is broken design.

## WCAG 2.2 POUR Principles

| Principle | Requirement | Key Rules |
|-----------|-------------|-----------|
| **Perceivable** | All content perceivable by all users | Text alternatives, captions, sufficient contrast, no color-only meaning |
| **Operable** | All functionality operable via all input methods | Keyboard accessible, no time traps, skip links, focus indicators |
| **Understandable** | Content and operation are understandable | Plain language, consistent navigation, specific error messages |
| **Robust** | Content works with current and future technologies | Valid HTML, ARIA roles used correctly, tested across assistive tech |

## Contrast Requirements

| Element | Minimum Ratio (AA) | AAA Target | Tool |
|---------|-------------------|------------|------|
| Body text (<18px / <14px bold) | **4.5:1** | 7:1 | WebAIM Contrast Checker |
| Large text (>=18px / >=14px bold) | **3:1** | 4.5:1 | Chrome DevTools |
| Non-text elements (icons, borders, focus rings) | **3:1** | -- | axe-core |
| Disabled elements | Exempt | -- | -- |
| Decorative elements | Exempt | -- | -- |

**Practical rule:** Test every foreground/background combination. Gray text on white is the most common failure -- `#767676` on `#fff` is the lightest gray that passes 4.5:1.

## Color Independence

Never rely on color alone to convey meaning. Provide redundant encoding for every color-coded element.

| Context | Bad (Color Only) | Good (Redundant Encoding) |
|---------|------------------|---------------------------|
| Status indicators | Red dot / green dot | Red dot + "Error" label / green dot + checkmark icon |
| Form validation | Red border on invalid field | Red border + error icon + error message text |
| Charts and data viz | Color-coded lines only | Color + pattern (dash, dot) + labeled legend |
| Links in body text | Color difference only | Color + underline (or underline on hover minimum) |
| Alerts and banners | Background color only | Background color + icon + role="alert" |

## Focus Indicators

Never remove `:focus` outlines without providing a replacement. Use `:focus-visible` to show focus rings only for keyboard users.

| Rule | Implementation |
|------|----------------|
| Never use `outline: none` without replacement | Remove only if custom focus style is applied |
| Use `:focus-visible` over `:focus` | Prevents focus rings on mouse clicks |
| Minimum focus ring | `3px solid` with `2px offset` in high-contrast color |
| Focus must be visible on all backgrounds | Test on light, dark, and colored backgrounds |
| Focus order must match visual order | Use `tabindex="0"`, avoid positive `tabindex` values |

## Keyboard Navigation

| Requirement | Implementation |
|-------------|----------------|
| All interactive elements reachable via Tab | Buttons, links, inputs, selects, custom widgets |
| Logical tab order | Matches visual left-to-right, top-to-bottom flow |
| Skip link as first focusable element | `<a href="#main" class="skip-link">Skip to content</a>` |
| Escape closes modals/dropdowns | Return focus to the trigger element |
| Arrow keys for composite widgets | Tabs, menus, radio groups, listboxes |
| No keyboard traps | Every focusable area can be exited via Tab or Escape |

## Touch Targets

Minimum touch target size is **44x44px** (WCAG 2.2 Level AA). Maintain **8px minimum spacing** between adjacent targets to prevent accidental activation.

| Element | Minimum Size | Minimum Spacing |
|---------|-------------|-----------------|
| Buttons | 44x44px | 8px |
| Links in navigation | 44px height | 8px vertical gap |
| Icon buttons | 44x44px (padding around smaller icons) | 8px |
| Inline text links | Exempt (but avoid dense clusters) | -- |

## Screen Reader Considerations

| Guideline | Rule |
|-----------|------|
| Heading hierarchy | `h1` through `h6` in logical order -- never skip levels |
| Landmark regions | `<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>` on every page |
| Alt text strategy | Informative images: describe content. Decorative images: `alt=""`. Complex images: `aria-describedby` linking to long description |
| Button labels | Avoid "Click here" -- use descriptive labels: "Download invoice PDF" |
| Form labels | Every input has a visible `<label>` with matching `for`/`id` |
| Live regions | `aria-live="polite"` for status updates, `aria-live="assertive"` for errors |
| Hidden content | Use `aria-hidden="true"` for decorative elements, `sr-only` class for screen-reader-only text |

## Cognitive Accessibility

- Use plain language -- grade 8 reading level maximum (Hemingway Editor)
- Consistent navigation placement across all pages
- Error messages must be specific: "Email must include @" not "Invalid input"
- Avoid auto-playing media -- always provide pause/stop controls
- Provide enough time -- no content that disappears after a fixed duration without user control

## Automated Testing

| Tool | Catches | Limitation |
|------|---------|------------|
| **axe-core** | ~30% of WCAG issues: contrast, missing labels, ARIA misuse | Cannot test visual layout, reading order, keyboard flow |
| **Lighthouse Accessibility** | Same engine as axe-core, scores 0-100 | Score of 100 does not mean accessible |
| **WAVE** | Visual overlay of issues on page | Cannot test dynamic content |

**Automated tools catch 30-50% of issues.** Manual testing is required for: keyboard navigation flow, screen reader experience, focus management in dynamic content, reading order, and cognitive clarity.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Color-only status indicators | Invisible to colorblind users (8% of males) | Add icon + text label |
| `outline: none` without replacement | Keyboard users cannot see focus | Use `:focus-visible` with custom ring |
| Placeholder-only labels | Disappear on input; not announced by all screen readers | Use visible `<label>` elements |
| Auto-playing video/audio | Disorienting; cannot be stopped by keyboard alone | Require user-initiated play |
| Missing heading hierarchy | Screen reader users cannot navigate by headings | Use `h1`-`h6` in logical order |
| `div` and `span` as buttons | No keyboard support, no screen reader role | Use `<button>` or add `role="button"` + `tabindex="0"` + keyboard handler |
| Positive `tabindex` values | Breaks natural focus order | Use `tabindex="0"` or `-1` only |

## Cross-Media Notes

- **Presentations:** Use high-contrast color schemes (projectors wash out colors). Provide alt text for all images in slide notes. Minimum 24px font for body text.
- **CVs/Resumes:** Use proper heading structure for screen reader navigation. Avoid tables for layout. Ensure the PDF is tagged and accessible (not just a flat image export).
- **Documents:** Generate accessible PDFs with tagged headings, alt text, and reading order. Test with a screen reader before distributing.

## Examples

Working implementations in `examples/`:
- **`examples/accessible-form-and-focus.md`** -- Accessible form with proper labels, focus indicators, error messaging, and ARIA attributes in CSS/HTML/React

## Review Checklist

When reviewing or building for accessibility:

- [ ] All text meets WCAG AA contrast ratios (4.5:1 body, 3:1 large text, 3:1 non-text)
- [ ] Color is never the sole indicator of meaning -- redundant encoding provided
- [ ] Every interactive element is reachable and operable via keyboard
- [ ] Focus indicators are visible on all backgrounds (3px solid minimum)
- [ ] `:focus-visible` used instead of `:focus` where appropriate
- [ ] Tab order matches visual reading order
- [ ] Skip link is the first focusable element on every page
- [ ] All images have appropriate alt text (informative or empty for decorative)
- [ ] Heading hierarchy is logical (h1-h6, no skipped levels)
- [ ] Landmark regions are present (`header`, `nav`, `main`, `footer`)
- [ ] Every form input has a visible `<label>` with matching `for`/`id`
- [ ] Touch targets are 44x44px minimum with 8px spacing
- [ ] No auto-playing media without user-initiated controls
- [ ] Error messages are specific and associated with their fields via `aria-describedby`
- [ ] axe-core or Lighthouse audit returns zero critical violations
