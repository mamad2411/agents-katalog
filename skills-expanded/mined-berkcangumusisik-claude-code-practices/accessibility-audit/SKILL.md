---
name: accessibility-audit
description: Audits React/HTML components for WCAG 2.1 accessibility issues
argument-hint: [file-or-directory]
user-invocable: true
allowed-tools: Read Grep Glob Edit
effort: medium
---

## Accessibility Audit (WCAG 2.1)

Target: **$1** (or `src/components/` if not specified)

Check each component for:

### Level A (Must Fix)
- Images missing `alt` attribute
- Form inputs without associated `<label>`
- Buttons with no accessible text (icon-only buttons need `aria-label`)
- Links with non-descriptive text ("click here", "read more")
- Missing `lang` attribute on `<html>`

### Level AA (Should Fix)
- Color contrast ratio < 4.5:1 for normal text (check CSS)
- Focus indicators removed (`outline: none` without alternative)
- Interactive elements not keyboard-reachable
- Missing `aria-expanded` on toggle elements
- Modal dialogs not trapping focus
- Missing skip navigation link

### Common React Issues
```tsx
// ❌ No accessible label
<button onClick={onClose}><XIcon /></button>

// ✅ Fixed
<button onClick={onClose} aria-label="Close dialog"><XIcon /></button>
```

For each issue:
- Severity: **Critical** (blocks screen readers) / **Major** / **Minor**
- File and line
- Fix with code example

Apply fixes after confirmation.
