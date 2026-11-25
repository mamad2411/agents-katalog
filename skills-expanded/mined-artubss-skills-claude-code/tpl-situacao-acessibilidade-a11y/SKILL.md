---
name: tpl-situacao-acessibilidade-a11y
description: Template do pack (situacao/19-acessibilidade-a11y.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/19-acessibilidade-a11y.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Accessibility Audit & Implementation

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/19-acessibilidade-a11y.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when auditing an application for accessibility (a11y) compliance, implementing WCAG 2.1 AA requirements, fixing specific accessibility issues found in user testing or automated audits, or building new UI components with accessibility-first. Accessibility is not a checkbox — it's a quality standard that improves usability for all users, including those using keyboards, screen readers, voice control, or operating in challenging visual conditions.

## OBJECTIVES
- Achieve WCAG 2.1 AA compliance across all user-facing interfaces
- Ensure keyboard-only users can complete all critical user flows
- Make all content usable with popular screen readers (NVDA, JAWS, VoiceOver)
- Meet minimum color contrast ratios for text and interactive elements
- Implement focus management that makes sense for keyboard users

## APPROACH RULES

1. **Semantic HTML first, ARIA second.** The most reliable way to convey meaning to assistive technology is semantic HTML: `<button>`, `<nav>`, `<main>`, `<h1>`…`<h6>`, `<label>`, `<table>`. Add ARIA only when HTML semantics are insufficient. Incorrect ARIA is worse than no ARIA.

2. **Every interactive element must be keyboard accessible.** Tab focus must reach all buttons, links, form fields, and interactive controls. Every focusable element must have a visible focus indicator. No keyboard traps (users can always navigate away).

3. **Focus management is mandatory for dynamic UI.** When a modal opens, focus moves into it. When it closes, focus returns to the trigger. When a new section loads (SPA navigation), focus moves to the content. Unmanaged focus makes screen readers disorienting.

4. **No information conveyed by color alone.** Error states need text labels, not just red borders. Status indicators need text or icons, not just colors. Add at least one non-color indicator for every color-coded meaning.

5. **All images need descriptive alt text.** Decorative images: `alt=""`. Informative images: `alt="A bar chart showing sales growth from 2023 to 2024"`. Never `alt="image"` or `alt="photo"`. Icon buttons: `aria-label="Close dialog"`.

6. **WCAG 2.1 AA minimum color contrast:** 4.5:1 for normal text, 3:1 for large text (18pt+ or 14pt+ bold), 3:1 for UI components (borders of form inputs, focus indicators). Test with real tools, not your eyes.

7. **Screen reader testing is required — automated tools find only ~30% of issues.** Test with: NVDA + Firefox (Windows), VoiceOver + Safari (macOS/iOS), TalkBack (Android). The goal: can a screen reader user complete all critical flows independently?

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| `<div onClick={...}>` as interactive element | Replace with `<button>` or `<a>`. If `<div>` must be used, add `role="button"`, `tabIndex={0}`, and keyboard handlers (`onKeyDown` for Enter/Space). |
| Missing form label | Add `<label htmlFor="fieldId">` or `aria-label`. `placeholder` is NOT a label substitute. |
| Icon-only button without text | Add `aria-label="[action]"` or `<span className="sr-only">Close</span>` |
| Color contrast failure | Darken text or lighten background. Use a contrast ratio tool to verify ≥ 4.5:1. |
| Popup/modal with no focus management | On open: `focus()` on first interactive element inside. On close: `focus()` on trigger element. Trap focus within. |
| Missing skip link | Add `<a href="#main-content" className="skip-link">Skip to main content</a>` as first focusable element |
| Animated content (auto-playing) | Add pause/stop control. Respect `prefers-reduced-motion` media query. |
| Error messages not associated with field | Add `role="alert"` to error container OR use `aria-describedby` linking field to error |
| Data table without headers | Add `<th scope="col">` for column headers, `<th scope="row">` for row headers |
| Custom dropdown/select component | This is complex. Either use native `<select>` (accessible by default) or implement full combobox ARIA pattern |

## WCAG 2.1 AA Checklist

### Perceivable
- [ ] All images have descriptive alt text (or `alt=""` for decorative)
- [ ] All audio/video has captions and/or transcripts
- [ ] Color is not the only way to convey information
- [ ] Text contrast ratio: ≥ 4.5:1 (normal), ≥ 3:1 (large text ≥18pt)
- [ ] UI component contrast ratio: ≥ 3:1 for borders, focus indicators
- [ ] Text can be resized to 200% without loss of content or functionality
- [ ] Content is not blocked by horizontal scrolling at 320px viewport width

### Operable
- [ ] All functionality available via keyboard
- [ ] No keyboard traps
- [ ] Skip navigation link present and functional
- [ ] Visible focus indicator on all focusable elements (not removed with `outline: none` without replacement)
- [ ] No content flashes more than 3 times per second (seizure risk)
- [ ] Page titles are descriptive and unique per page
- [ ] Link text describes destination (no "click here", "read more")
- [ ] Focus order is logical (matches visual reading order)

### Understandable
- [ ] Language of page set: `<html lang="en">`
- [ ] Language changes marked: `<span lang="fr">Bonjour</span>`
- [ ] Form inputs have labels visible at all times
- [ ] Error messages identify: what went wrong + how to fix it
- [ ] No unexpected context changes on focus or input

### Robust
- [ ] Valid HTML (no duplicate IDs, properly nested elements)
- [ ] Custom components have correct ARIA roles, states, and properties
- [ ] Status messages (`role="alert"`, `aria-live`) announced to screen readers without receiving focus

## Focus Indicator (CSS)

```css
/* ✅ Good: visible focus indicator */
:focus-visible {
  outline: 2px solid #0066CC;
  outline-offset: 2px;
  border-radius: 2px;
}

/* ❌ Bad: removes all focus indicators */
* {
  outline: none;
}

/* Screen reader only utility class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

## Modal Focus Management (React)

```tsx
import { useEffect, useRef } from 'react'

function Modal({ isOpen, onClose, title, children }) {
  const modalRef = useRef<HTMLDivElement>(null)
  const triggerRef = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (isOpen) {
      triggerRef.current = document.activeElement as HTMLElement
      // Move focus to first interactive element in modal
      const firstFocusable = modalRef.current?.querySelector<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      firstFocusable?.focus()
    } else {
      // Return focus to trigger when modal closes
      triggerRef.current?.focus()
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <h2 id="modal-title">{title}</h2>
      {children}
      <button onClick={onClose} aria-label="Close dialog">×</button>
    </div>
  )
}
```

## DO NOT

- **DO NOT** use `outline: none` or `outline: 0` without providing an alternative visible focus indicator
- **DO NOT** use `placeholder` as a label — it disappears when the user types
- **DO NOT** rely only on automated tools (axe, Lighthouse) — they find ~30% of real issues
- **DO NOT** add `role="button"` to a `<div>` without also adding `tabIndex={0}` and keyboard handlers
- **DO NOT** convey error state through color alone — add an error message or icon
- **DO NOT** use `aria-label` to override visible text — confuses users who can both see and use a screen reader
- **DO NOT** auto-focus a form field on page load in a way that skips past important page context
- **DO NOT** use `tabIndex` > 0 (e.g., `tabIndex={3}`) — it creates confusing non-linear tab order

## OUTPUT FORMAT

For each accessibility audit, produce:

**Accessibility Audit Report:**
```markdown
## Accessibility Audit Report

**Date:** 2024-01-15
**Scope:** Checkout flow (5 pages)
**WCAG Level:** 2.1 AA
**Tools Used:** axe DevTools + manual keyboard testing + VoiceOver

### Summary
| Severity | Count |
|----------|-------|
| Critical | 3 |
| Serious | 7 |
| Moderate | 12 |
| Minor | 5 |

### Critical Issues (Must Fix)
#### 1. Missing form labels on checkout address form
- WCAG Criterion: 1.3.1 Info and Relationships (Level A)
- Element: `<input id="street-address">` (no associated label)
- Impact: Screen reader users hear "edit text" with no context
- Fix: Add `<label for="street-address">Street Address</label>`
- Files: CheckoutAddressForm.tsx:34

### Keyboard Navigation
- [x] Tab through checkout: All fields reachable ✅
- [ ] Modal focus: Focus not trapped in order confirmation modal ❌
- [ ] Skip link: Missing ❌

### Color Contrast Failures
| Element | Foreground | Background | Actual Ratio | Required |
|---------|-----------|-----------|--------------|----------|
| Help text | #999999 | #FFFFFF | 2.85:1 | 4.5:1 |
| Disabled button text | #AAAAAA | #EEEEEE | 1.9:1 | 3:1 |
```

## QUALITY GATES

- [ ] Automated tool (axe or Lighthouse) shows zero Critical and zero Serious violations
- [ ] Full tab navigation through all critical user flows completed without mouse
- [ ] All form fields have visible, persistent labels (not just placeholder)
- [ ] Modal/dialog focus management tested: open → focus in, close → focus returns
- [ ] Color contrast verified for all text elements (≥ 4.5:1 normal, ≥ 3:1 large)
- [ ] All images have appropriate alt text (not "image" or filename)
- [ ] `<html lang="...">` set correctly on all pages
- [ ] Skip link present and navigates to `<main>` correctly
- [ ] Screen reader test (VoiceOver or NVDA) completed on checkout flow
- [ ] `prefers-reduced-motion` respected for all animations
