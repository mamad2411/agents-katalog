---
name: responsive-god
description: Audit and fix responsive formatting problems in web apps, React components, Tailwind layouts, forms, tables, nav, typography, safe-area mobile shells, Storybook stories, and Playwright or visual-regression coverage. Use when asked to inspect responsive design, mobile layout bugs, viewport/container breakage, iOS form zoom, overflow, cramped UI, mobile parity, or to implement selected responsive fixes.
---

# Responsive God

Responsive God is a design-engineering workflow for finding and repairing responsive formatting failures. It is not a vague visual critique helper. It inspects the actual app, routes, components, styles, stories, and tests before making claims. It ranks likely breakage, identifies viewport and container conditions, explains root causes, proposes minimal patches, and adds Storybook plus Playwright or visual-regression coverage that prevents regressions.

## Command Interface

Primary commands:

```bash
responsive-god audit <target-or-url>
responsive-god audit-platform [--routes routeA,routeB]
responsive-god audit-component <component-or-file>
responsive-god scan <path> [--json]
responsive-god plan <ids>
responsive-god implement <ids> [--with-stories] [--with-tests]
responsive-god verify <target-or-url>
responsive-god doctor <file-or-route>
```

Natural language works too:

- "Audit the platform for responsive formatting problems."
- "Audit this component at mobile, tablet, desktop, and narrow container widths."
- "Find why this form zooms on iOS and patch it."
- "Implement RESP-H001 and RESP-H004 with Storybook and Playwright coverage."
- "Check mobile parity after this desktop layout change."

## First Action

Load `workflows/00-command-router.md`, then load only the workflow and reference files required for the user request.

For HypeStake or other repo-specific work, follow the repo's local agent instructions first. If the repo maintains a wiki or harness, read the relevant index or harness docs before editing product code.

## Operating Model

1. Decode the user request and identify the mode.
2. Inspect relevant files before judging them.
3. Run the deterministic scanner when a local code target exists.
4. If a route or local app is available, use browser inspection at the requested or obvious target.
5. Audit both viewport widths and component container widths.
6. Rank issues by user impact, likelihood, confidence, and fix size.
7. For audits, return numbered issue IDs and wait for approval or selected IDs before editing.
8. For implementation, patch only the selected IDs unless a small shared utility change is required.
9. Add or update Storybook stories for narrow, medium, wide, empty, loading, error, and long-content states when Storybook exists or is requested.
10. Add or update Playwright, visual-regression, or component tests when the project has a test surface that can support them.
11. Verify with typecheck, lint, tests, build, and browser screenshots as appropriate for the changed files.

## Non-Negotiables

- Read the target files before proposing or applying patches.
- Do not invent routes, components, scripts, or design-system primitives.
- Do not rewrite unrelated layouts or global styles to fix one component.
- Do not remove working desktop behavior while fixing mobile.
- Do not hide important content behind progressive disclosure just to make it fit.
- Do not accept horizontal page scroll as a fix unless the component is intentionally scrollable, such as a data table or media scroller.
- Do not rely on viewport screenshots alone for reusable components. Audit embedded container widths too.
- Do not use fixed widths when `minmax()`, `auto-fit`, `flex-wrap`, intrinsic sizing, or container queries solve the problem.
- Do not ship mobile form controls below `16px` effective font size.
- Do not add `maximum-scale=1` or disable zoom to work around iOS input zoom.
- Do not position bottom or corner controls without considering `env(safe-area-inset-*)` when the page uses or should use edge-to-edge mobile layout.
- Do not ship unlabelled icon-only disclosure controls unless the component already has an accessible label and visible context.
- Do not expose raw internal debug overlays to production users.
- Preserve accessibility, focus order, keyboard behavior, and mobile tap targets.

## Required Audit Output

For `audit`, `audit-platform`, `audit-component`, and `doctor`, output:

1. One-sentence diagnosis.
2. Ranked issue table with stable IDs such as `RESP-H001`, `RESP-M003`, and `RESP-L002`.
3. For each issue: severity, evidence, likely failing widths or container conditions, root cause, user impact, minimal patch, files/selectors, story coverage, test coverage, confidence, and acceptance criteria.
4. A separate "Viewport and Container Matrix" listing widths and embedded conditions most likely to fail.
5. A "Storybook Plan" with narrow, medium, wide, empty, loading, error, long-content, and role/permission states when relevant.
6. A "Regression Test Plan" with Playwright or visual-regression scenarios.
7. A "Patch Plan" sorted by safest implementation order.
8. Suggested next command: "Reply with the IDs to implement."

## Required State

Maintain this state during the workflow:

```text
command:
target:
mode:
repo_type:
framework:
style_system:
storybook_present:
playwright_present:
routes_or_components:
scanner_findings:
browser_findings:
responsive_matrix:
numbered_issues:
selected_ids:
files_changed:
stories_changed:
tests_changed:
verification:
open_questions:
```

## Severity System

- `RESP-H###`: High risk. Blocks core task, hides or overlaps important controls, causes page-level overflow, breaks forms on mobile, makes admin/finance/deal flows unsafe, or affects a high-traffic route.
- `RESP-M###`: Medium risk. Noticeable layout degradation, cramped content, weak affordance, missing long-content state, missing mobile/tablet parity, or likely failure under common data.
- `RESP-L###`: Low risk. Polish issue, future brittleness, narrow edge case, or improvement that should be bundled with nearby changes.
- `RESP-R###`: Radical or structural idea. Useful when a surface needs a bigger redesign, but never implement without explicit approval.

## Local Scanner Helper

Use the deterministic helper when available:

```bash
node scripts/responsive-god.mjs scan .
node scripts/responsive-god.mjs scan src --json
node scripts/responsive-god.mjs inspect-file src/components/Example.tsx
node scripts/responsive-god.mjs matrix
```

The scanner is evidence-gathering. The agent remains responsible for reading code, understanding design intent, producing minimal patches, and verifying visual behavior.

## Source Rubric

The embedded rubric is distilled from the user's responsive design references:

- macro layouts should start from a sensible single-column source order and grow into grid or flex only when there is room.
- micro layouts should adapt to their container, not only to the viewport.
- Tailwind is mobile-first: unprefixed utilities are the mobile baseline; breakpoint prefixes apply at that breakpoint and up.
- forms should combine correct `type`, `inputmode`, and `autocomplete` for mobile keyboards and autofill.
- iOS Safari zooms focused inputs when effective text is below 16px.
- safe-area insets protect fixed and edge-to-edge UI from notches, dynamic islands, rounded corners, and home indicators.
- overflow patterns for nav, carousels, and tables need visible affordances.
- typography should use bounded fluid sizing, readable line lengths, unitless line-height, and long-string protection.

