---
name: skill-accessibility
description: WCAG 2.1 AA compliance, keyboard navigation, screen reader testing, semantic HTML, ARIA labels, color contrast, assistive technology validation. Use when ensuring accessibility, conducting a11y audits, testing with screen readers, or designing inclusive interfaces.
version: 1.0.0
---

# Skill: Accessibility (WCAG 2.1 AA)

Ensure your product is usable by everyone, including people with disabilities. Accessibility is a feature, not optional.

## WCAG 2.1 AA Checklist

**Perceivable**
- [ ] Images have meaningful alt text
- [ ] Videos have captions
- [ ] Color is not the only way to convey info
- [ ] Text contrast ≥ 4.5:1 (normal), ≥ 3:1 (large)
- [ ] Content can be resized 200% without loss
- [ ] No flashing > 3x/second

**Operable**
- [ ] Keyboard accessible (Tab, Enter, Space, Arrows)
- [ ] Focus visible (outline or custom)
- [ ] Focus order logical (top→bottom)
- [ ] No keyboard traps
- [ ] Enough time to read content
- [ ] Navigable (headings, landmarks, skip links)

**Understandable**
- [ ] Language identified
- [ ] Instructions clear
- [ ] Form labels + error messages
- [ ] Consistent navigation

**Robust**
- [ ] Valid semantic HTML
- [ ] Heading hierarchy valid (h1 → h2/h3, no skips)
- [ ] ARIA only when HTML insufficient
- [ ] Works with assistive tech

## Semantic HTML

```html
<!-- ✓ Use semantic tags -->
<nav>Navigation</nav>
<main>Content</main>
<article>Post</article>
<section>Section</section>
<aside>Related</aside>

<!-- ✓ Form labels -->
<label for="email">Email</label>
<input id="email" type="email" />

<!-- ✓ Heading hierarchy -->
<h1>Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

## Keyboard Testing

1. Hide mouse
2. Tab through entire page
3. Check: Focus visible, order logical, no traps
4. Test: Enter (buttons), Space (toggles), Arrows (menus)

## Screen Reader Testing

- NVDA (free, Windows): Ctrl+Alt+N
- VoiceOver (Mac): Cmd+F5
- Mobile: TalkBack (Android), VoiceOver (iOS)

## Color Contrast

- Text: 4.5:1 minimum (white text on dark blue too light)
- Large text (18pt+): 3:1 minimum
- Use: WebAIM contrast checker

## Testing Tools

- **Automated**: axe, WAVE, Lighthouse
- **Manual**: Screen reader, keyboard-only
- **CI**: axe in Playwright tests

## Success

- WCAG 2.1 AA compliant
- Keyboard usable (no mouse)
- Screen reader tested
- Zero high/critical violations
- Contrast ≥ 4.5:1

---

**Status**: Ready for accessibility work  
**Best for**: A11y audits, accessible design, WCAG compliance
