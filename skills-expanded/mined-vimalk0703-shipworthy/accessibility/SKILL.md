---
name: accessibility
description: WCAG 2.1 AA baseline — semantic HTML, ARIA labels, color contrast, keyboard navigation, screen reader compatibility, and focus management.
invoke_when: Use when writing JSX/TSX, HTML templates, UI components, or any user-facing interface that requires WCAG compliance.
---

# Accessibility

## Baseline: WCAG 2.1 AA

Every user-facing interface must meet WCAG 2.1 Level AA. This is not optional — it's a legal requirement in many jurisdictions and the right thing to do.

## Semantic HTML

Use the correct element, not a styled div:
- `<button>` for actions (not `<div onClick>`)
- `<a>` for navigation (not `<span onClick>`)
- `<nav>` for navigation regions
- `<main>` for primary content
- `<header>`, `<footer>`, `<section>`, `<article>` for document structure
- `<h1>`-`<h6>` in proper order (no skipping levels)
- `<ul>`/`<ol>` for lists
- `<table>` for tabular data (not for layout)

## ARIA Labels

- Every interactive element needs an accessible name
- `aria-label` for elements without visible text
- `aria-labelledby` to reference visible text
- `aria-describedby` for additional context
- `aria-hidden="true"` for decorative elements
- Never use ARIA when native HTML semantics suffice

## Color and Contrast

- Text contrast ratio: 4.5:1 minimum (3:1 for large text)
- Never convey information through color alone (add icons, text, patterns)
- Ensure focus indicators are visible against all backgrounds

## Keyboard Navigation

- Every interactive element reachable via Tab
- Logical tab order (follows visual layout)
- `Escape` closes modals/popups
- `Enter`/`Space` activates buttons
- Arrow keys for menus, tabs, and lists
- Visible focus indicator on all interactive elements

## Images

- Meaningful images: `alt` text describing the content
- Decorative images: `alt=""` (empty alt, not missing alt)
- Complex images (charts, diagrams): detailed `aria-describedby`

## Forms

- Every input has a `<label>` (linked via `for`/`id`)
- Error messages linked to inputs via `aria-describedby`
- Required fields marked with `aria-required="true"`
- Form validation errors announced to screen readers

## Focus Management

- When modals open, focus moves to the modal
- When modals close, focus returns to the trigger
- Focus trapped inside modals (can't tab to background)
- Route changes announce the new page to screen readers
