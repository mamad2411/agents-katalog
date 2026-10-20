---
name: accessibility
description: Check and improve accessibility for web and app UI: semantic HTML, keyboard navigation, focus management, accessible names, ARIA, forms, dialogs, error messaging, color contrast, motion preferences, and WCAG 2.2 AA-oriented implementation.
---

# Accessibility

## Workflow

1. Prefer native semantic elements before ARIA.
2. Ensure every interactive control is keyboard reachable and has visible focus.
3. Provide accessible names and descriptions for controls, icons, inputs, and regions.
4. Make form errors programmatically associated with fields.
5. Ensure dialogs, menus, tabs, and composite widgets follow expected keyboard behavior.
6. Respect reduced motion and avoid relying only on color.

## Checks

- Page has correct landmarks and heading order.
- Buttons are buttons; links navigate.
- Focus is not trapped except in modal contexts, and then only intentionally.
- Disabled, loading, and error states remain perceivable.
- Contrast is sufficient for text and essential UI.

## Output

Mention concrete accessibility fixes and how to verify them by keyboard or automated tooling.
