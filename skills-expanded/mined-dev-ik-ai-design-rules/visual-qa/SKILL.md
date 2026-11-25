---
name: visual-qa
description: Use when an implemented screen, screenshot, or UI change needs visual QA for spacing, alignment, wrapping, clipping, overlap, hierarchy, component states, or comparison with a supplied design reference. Skip backend-only changes.
---

# Visual QA

Review observed UI against the user's task, existing design system, and retrieved graph context. This execution skill complements `design-reviewer`, which owns the final traceability review.

## Inputs and capabilities

Identify the screen, primary action, changed components, relevant states, target devices, and any supplied reference. Retrieve focused context with `npx --no-install ai-design-context context --review "<graph ID or matching phrase>" --intent qa`; read the returned research and rules. An arbitrary application path is not automatically a graph match.

Record which tools are actually available:

- A browser tool or the project's existing Playwright setup for navigation, viewport changes, clicks, keyboard input, scrolling, DOM measurements, and screenshots.
- An image-viewing tool and an image-capable model for inspecting captured pixels and references.
- Source and DOM inspection for relating a visible issue to its implementation.

If a capability is unavailable, continue with the available evidence and mark the missing checks **unverified**. Skills do not install browser binaries, provision model vision, or enable MCP tools. A code-only review cannot establish rendered quality; a screenshot cannot establish keyboard or responsive behavior.

## Browser and image loop

1. Open the actual implementation. Record its URL or fixture path, browser, viewport in CSS pixels, theme, zoom, data, and state. Exercise the primary action and relevant default, loading, empty, error, success, and disabled states; mark inapplicable states with a reason.
2. Check narrow and wide layouts with `responsive-check`. Open and close menus, dialogs, and sheets, scroll past sticky regions, and exercise keyboard focus with `accessibility-check`.
3. Save viewport screenshots for geometry and separate full-page screenshots for long content. Use the project's evidence convention; otherwise create a dated review folder under `output/playwright/`. Record the steps that reproduce each capture.
4. Open the captured images, not just their filenames. Inspect alignment, spacing consistency, typography, line breaks, clipped text, collisions, icon alignment, button/input sizing, content density, primary-action prominence, and state feedback. Confirm suspected geometry problems with DOM measurements where possible.
5. If a design reference exists, compare matching viewport, state, theme, content, and scale. Record unmatched conditions instead of attributing every pixel difference to a defect. Without a reference, assess task clarity and existing tokens; do not invent a target composition from taste.
6. For authorized fixes, make a focused patch, repeat the failed interaction, and recapture the same conditions. Run the project's relevant code checks. Preserve product logic and the existing UI stack.

## Report contract

Lead with **PASS**, **NEEDS WORK**, or **PARTIAL**, scoped to the surfaces and states actually reviewed. PARTIAL means missing evidence prevents completing that scope. Separate observed defects from coverage gaps; a skipped check is not a confirmed product defect.

For each finding, include:

| Field | Required evidence |
| --- | --- |
| ID and severity | Stable review-local ID; Critical, Major, Minor, or Polish based on impact on the primary task. |
| Surface and conditions | Screen/component, viewport, data/state, and input method. |
| Reproduction | Actions another reviewer can repeat. |
| Observed / expected | What happened; applicable rule, pattern, reference, or explicit knowledge gap. |
| Evidence | Screenshot path and inspected region; DOM measurement or interaction observation when available. |
| Impact and fix | User consequence, focused correction, likely file/component when verified. |
| Retest | Outcome and matching after-capture, or pending. |

Finish with a coverage table: **surface | viewport | state/input | evidence | checked/unverified/not applicable**. List missing tools and any reference-comparison gaps. Do not infer a global pass from one desktop screenshot.

## Graph anchors and tool references

- `CHECK-00001` / `checklists/DESIGN_QA.md`: state, responsive, accessibility, and evidence boundaries.
- `RULE-00008` / `VIS-001`: existing semantic tokens.
- `RULE-00014` / `VIS-002`: content and primary-action hierarchy.
- `RULE-00011` / `PERF-001`: loading-state layout stability.
- [Playwright screenshots](https://playwright.dev/docs/screenshots) and [emulation](https://playwright.dev/docs/emulation) describe capture and viewport capabilities, not proof that those tools are installed.
