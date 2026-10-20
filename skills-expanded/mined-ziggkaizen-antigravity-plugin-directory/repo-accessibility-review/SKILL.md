---
name: repo-accessibility-review
description: Reviews frontend code for accessibility across semantic structure, keyboard support, focus management, labels, ARIA usage, contrast, forms, dynamic content, and motion. Use when editing or reviewing UI controls, forms, dialogs, navigation, or user-facing markup.
---


# Repository Accessibility Review

Use this skill to review or improve accessibility in browser-facing code.

## Review Areas

- semantic markup
- accessible names and descriptions
- keyboard operation
- focus visibility and management
- ARIA correctness
- forms and validation messages
- dialogs, menus, popovers, and overlays
- color contrast and color-independent meaning
- reduced motion
- dynamic content announcements

## Required Behavior

- Prefer native semantics over custom controls.
- Do not add ARIA blindly.
- Check keyboard flow for interactive UI.
- Consider screen-reader-visible names, states, and relationships.
- Report unverified assistive-technology behavior honestly.

## Workflow

Use `workflows/accessibility-review-workflow.md`.

## Resources and Examples

- `resources/accessibility-checklist.md`
- `examples/accessibility-feedback-examples.md`

## Scripts

This skill owns:

```text
scripts/accessibility-pattern-scan.py
```

Run with `--help` before manual use.

