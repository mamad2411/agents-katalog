---
name: accessibility
description: File-level accessibility audit with concrete line locations for every finding. Eight rules: img-missing-alt, button-without-label, link-without-text, input-without-label, positive-tabindex, click-handler-on-non-interactive, autofocus, low-contrast-token-pair. Use when the user wants to audit a11y, find accessibility regressions, or gate a PR on a11y. Run as `node ~/.claude/skills/dragoon/skills/accessibility/scripts/accessibility.js [path]`.
version: 1.0.0
---

# /accessibility

Goes deeper than the aggregate score in `/critique`. Per-element, per-line findings.

## When to use

- Pre-launch accessibility audit
- The user says "a11y check", "accessibility audit", "WCAG check"
- After a feature lands, before merging

## Rules

- `a11y-001` img-missing-alt (high)
- `a11y-002` button-without-label (high)
- `a11y-003` link-without-text (high)
- `a11y-004` input-without-label (high)
- `a11y-005` positive-tabindex (medium)
- `a11y-006` click-handler-on-non-interactive (medium)
- `a11y-007` autofocus (low)
- `a11y-008` low-contrast-token-pair, contrast < WCAG AA 4.5:1 (medium)

Each finding includes file, line, column, snippet, message, and a concrete fix.

## Run it

```
dragoon accessibility                       # everything
dragoon accessibility --severity high       # only critical
dragoon accessibility src/components        # one folder
dragoon accessibility --rules               # list every rule
dragoon accessibility --json                # CI mode
```
