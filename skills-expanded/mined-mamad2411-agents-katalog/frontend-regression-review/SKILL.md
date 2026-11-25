---
name: "frontend-regression-review"
description: "Review UI and frontend changes for regressions in layout, accessibility, loading or error states, responsiveness, and interaction flow. Use when a user asks for frontend regression review, UI risk analysis, release polish checks, or as part of $full-test-suite deep-audit work."
---

# Frontend Regression Review

Look for concrete frontend regressions, not just design opinions.

## Focus Areas

- broken layout on common breakpoints
- missing loading, empty, and error states
- accessibility regressions
- interaction dead ends or state desynchronization
- UI behavior that diverges from current flow assumptions

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Verification template: `../_shared-project-ops/references/verification-template.md`
