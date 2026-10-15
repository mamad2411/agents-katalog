---
name: responsive-layout-review
description: Review and improve responsive layouts across mobile, tablet, desktop, web apps, SaaS dashboards, marketing pages, and desktop-like utilities. Use when designing breakpoints, adaptive navigation, grids, density, sidebars, tables, modals, keyboard states, or layouts that must work from small screens to wide monitors.
---

# Responsive Layout Review

Use this skill to make layouts adapt by intent, not by arbitrary breakpoints.

## Workflow

1. Identify content hierarchy, primary task, and supported viewport/device classes.
2. Read `references/responsive-layout-rules.md`.
3. Review layout states: compact, medium, wide, high-density, keyboard, zoom, and reduced width.
4. Check navigation, tables, forms, modals, media, and empty/error states.
5. Produce breakpoint strategy, issues, and acceptance checks.

## Guardrails

- Breakpoints should follow content stress points, not only device names.
- Do not hide critical actions on small screens.
- Preserve keyboard, focus, zoom, and screen-reader usability.

## Output format

```text
Surface:
Primary task:

Responsive strategy:
- <layout state> -> <behavior>

Findings:
- <rule id> <issue> -> <fix>

Acceptance checks:
- <viewport/state check>
```
