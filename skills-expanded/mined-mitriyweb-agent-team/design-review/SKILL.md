---
name: design-review
description: Review UI implementation for pixel-perfection and accessibility.
compatibility: Requires bash, Claude Code
metadata:
  team: frontend
  role: design-reviewer
  version: "1.0"
---

## Procedure

1. Receive the implementation or PR from the frontend-dev.
2. Perform visual review for pixel-perfection and "WOW" factor using `references/aesthetics-checklist.md`.
3. Check for WCAG 2.1 AA accessibility compliance using `references/wcag-checklist.md`.
4. Report findings to the developer with specific references to the design system and checklists.

## Gotchas

- Refer to `references/wcag-checklist.md` for the accessibility baseline.
- WCAG 2.1 AA is the project's baseline.

## Validation loop

The design-reviewer ensures that all UI changes are visually correct and accessible before passing to QA.
