---
name: wp-classic-theme-accessibility-i18n
description: Reviews WordPress classic themes for semantic HTML, keyboard access, focus behavior, accessible names, translation functions, text-domain consistency, and localization readiness. Use before release or when changing user-facing markup and strings.
license: MIT
compatibility: "General accessibility and internationalization guidance."
---

# WordPress Classic Theme Accessibility and Internationalization

## Use this skill when

- Adding or changing navigation, forms, dialogs, controls, or content markup.
- Adding user-facing strings.
- Preparing a theme for translation or WordPress.org review.
- Reviewing editor and frontend accessibility.
- Investigating keyboard, focus, contrast, or screen-reader issues.

## Workflow

Use [accessibility-i18n-review-workflow.md](workflows/accessibility-i18n-review-workflow.md).

## Resources

- [accessibility-review-checklist.md](resources/accessibility-review-checklist.md)
- [internationalization-checklist.md](resources/internationalization-checklist.md)

## Principles

- Use native semantic elements before ARIA.
- Preserve keyboard access and visible focus.
- Do not use placeholder text as the only label.
- Keep heading hierarchy meaningful.
- Provide useful alternative text policy for theme-owned images.
- Internationalize user-facing source strings, not user content.
- Escape translated strings for their final output context.
