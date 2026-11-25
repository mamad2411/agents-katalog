---
name: responsive-check
description: Use when a screen must be checked across mobile, tablet, laptop, or desktop sizes for overflow, wrapping, sticky overlaps, collapsed navigation, unreachable actions, sheets, dialogs, tables, filters, or charts. Skip non-UI maintenance.
---

# Responsive Check

Verify adaptation through browser behavior and inspected screenshots. This execution skill complements `mobile-ux-expert`, which guides touch-first product decisions.

## Scope and preparation

Identify the target devices, primary task, changed breakpoints, long-content cases, and relevant states. Retrieve focused graph context with `--platform mobile` and read the applicable research and rules. Use the project's actual breakpoints and device targets. Example CSS viewports for exploratory sampling are 390x844, 768x1024, and 1440x900; include narrower widths and just below/above affected breakpoints when the product supports them. These samples are not universal layout rules or a substitute for actual devices.

Use available browser tools or the project's existing Playwright setup. Record viewport dimensions, scale, theme, data, and state. If browser access is absent, provide a source/screenshot-limited review and mark unseen widths and interactions unverified.

## Execute

1. Load the same flow at each selected width. Exercise capture/navigation, open and close sheets or dialogs, and scroll through long content and sticky regions.
2. Check horizontal page overflow, broken grids, long labels and entries, clipped text, navigation collapse, hidden primary actions, oversized dialogs, and controls obscured by sticky elements. For tables/charts, distinguish intentional bounded horizontal scrolling from accidental page overflow.
3. Observe wrapping and control placement before and after state changes, including loading, validation errors, retry, and success. Compare geometry when `PERF-001` applies.
4. Inspect images of each captured state and confirm suspected bounds with DOM measurements. Judge touch targets using the clickable area and the graph's `A11Y-001`, not icon dimensions alone.
5. For mobile input flows, record whether a real virtual keyboard was exercised. Desktop viewport emulation does not prove keyboard resizing, safe-area handling, or physical-device touch behavior. Mark those as gaps if relevant and untested.
6. After authorized fixes, repeat the failing width, relevant neighboring breakpoint, and affected wide layout. Capture before/after evidence under matching conditions.

## Output

Return a **scoped verdict**, then **viewport | state/action | observed behavior | screenshot/measurement | checked/unverified/not applicable**. Each confirmed issue includes severity, reproduction, user impact, graph/reference basis, focused fix, and verified component/file when known. Report breakpoint behavior and physical-device gaps separately. A screenshot at one size is not a responsive pass.

Sources: `CHECK-00001`, `RULE-00005` / `UX-001`, `RULE-00009` / `A11Y-001`, `RULE-00011` / `PERF-001`, and their retrieved source research. Use [Playwright emulation](https://playwright.dev/docs/emulation) for tool mechanics; it does not replace device evidence.
