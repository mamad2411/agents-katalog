---
name: accessibility-checklist
description: Verify WCAG 2.1 AA compliance for UI components. Use when building or reviewing frontend components, implementing accessibility, or working with frontend-architect.
---

# Accessibility Checklist

## Quick Checks

### Semantic HTML
- [ ] Use `<button>` for actions, `<a>` for navigation
- [ ] Use headings in order (h1 → h2 → h3)
- [ ] Use `<label>` for form inputs; associate with `htmlFor`/`id`
- [ ] Use `<main>`, `<nav>`, `<aside>`, `<footer>` for landmarks

### Keyboard
- [ ] All interactive elements focusable (no `tabIndex="-1"` on controls)
- [ ] Focus order is logical
- [ ] Focus visible (outline or custom ring)
- [ ] Escape closes modals/dropdowns
- [ ] No keyboard traps

### Screen Readers
- [ ] Images have `alt` (empty `alt=""` for decorative)
- [ ] Form errors announced (aria-live or role="alert")
- [ ] Dynamic content changes announced
- [ ] Use `aria-label` or `aria-labelledby` when visible label insufficient

### Color & Contrast
- [ ] Text contrast ≥ 4.5:1 (normal), ≥ 3:1 (large)
- [ ] Don't rely on color alone for information
- [ ] Focus indicators visible

### Forms
- [ ] Required fields indicated (aria-required, visual)
- [ ] Error messages linked to fields (aria-describedby)
- [ ] Clear, inline validation feedback

### Testing
- Navigate with keyboard only
- Test with screen reader (VoiceOver, NVDA)
- Use axe DevTools or Lighthouse accessibility audit
