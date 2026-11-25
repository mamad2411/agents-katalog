---
name: web-accessibility-audit
description: Audits UI code against WCAG 2.2 for keyboard access, labels, contrast and focus handling, and fixes what it finds. Use it on any page or component.
---

# Web accessibility audit

Check the code against WCAG 2.2 level AA. Prefer native HTML over ARIA.

## Steps

1. Read the component and its styles. Note every interactive element and every image, icon, form field, heading and landmark.
2. Keyboard (2.1.1, 2.4.7): everything clickable must be a real `button` or `a href`, reachable with Tab, activated with Enter or Space, and show a visible focus ring. Flag `div onClick`, `tabindex>0` and `outline: none` without a replacement.
3. Names (4.1.2, 1.1.1): each control needs an accessible name: a `label for`, text content or `aria-label`. Icon-only buttons need one. Images need meaningful `alt`, or `alt=""` when decorative.
4. Forms (3.3.1, 3.3.2): labels visible, errors in text linked with `aria-describedby`, required fields marked in text, no hint text standing in for a label.
5. Structure (1.3.1): one `h1`, no skipped heading levels, landmarks (`main`, `nav`), lists as lists, tables with `th scope`.
6. Contrast (1.4.3, 1.4.11): compute ratios from the actual hex values: 4.5:1 for text, 3:1 for large text and UI borders. Do not judge by eye.
7. Dynamic content: dialogs trap focus and return it on close, `Escape` closes, status messages use `role="status"`, no motion without `prefers-reduced-motion`.
8. If a dev server is available, tab through the page and run axe or Lighthouse as a second check.

## Report

A table: file:line, criterion, problem, fixed snippet. Apply fixes only when asked; otherwise list them. Say what needs a human with a screen reader.
