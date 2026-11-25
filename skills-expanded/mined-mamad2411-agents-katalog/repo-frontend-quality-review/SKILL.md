---
name: repo-frontend-quality-review
description: Reviews frontend changes for accessibility, responsive behavior, browser compatibility, UX states, client security, privacy, performance, maintainability, and user-visible regressions. Use for UI components, pages, forms, navigation, styling, and frontend diffs.
---


# Repository Frontend Quality Review

Use this skill when reviewing or implementing frontend changes in any framework or stack.

## When to Use This Skill

Use this skill for UI components, pages, forms, navigation, CSS/layout, design-system usage, client-side state, browser-facing error handling, and frontend regression investigation.

## Review Focus

1. User-visible behavior
2. Accessibility
3. Responsive and browser behavior
4. UX states
5. Client-side security and privacy
6. Performance
7. Maintainability
8. Test and validation evidence

## Required Behavior

- Inspect relevant UI code before suggesting changes.
- Avoid framework-specific advice unless repository conventions establish it.
- Identify which behavior was verified and which behavior remains unverified.
- Provide specific, actionable review comments.
- Prefer small, user-centered fixes over broad rewrites.

## Workflow

Use `workflows/frontend-quality-review-workflow.md` for general frontend diff review.

## Resources and Examples

- `resources/frontend-quality-checklist.md`
- `examples/frontend-review-comment-examples.md`

## Scripts

This skill owns:

```text
scripts/frontend-quality-scan.py
scripts/frontend-quality-stop-reminder.py
```

Run scripts with `--help` before manual use.

