---
name: mobile-wireframe
description: Convert a validated mobile UX architecture into low-fidelity screen and interaction structure before visual styling. Use when Codex needs wireframes, layout hierarchy, content priority, task-state coverage, overlay behavior, or a visual-agnostic handoff between UX architecture and UI design.
---

# Mobile Wireframe

Define the screen skeleton and interaction hierarchy without choosing colors, typography, imagery, or decorative style.

## Establish the input contract

Prefer `ux-architecture.json` plus `product-brief.json`. Validate upstream artifacts when validators exist. Preserve upstream Requirement, Flow, Screen, and State IDs. If the architecture is incomplete, record the gap rather than inventing a polished screen.

## Build the wireframe

For each screen:

1. State the single user question and primary task.
2. Order the safe-area, navigation, context, content, action, and feedback regions.
3. Assign each region a semantic role, content pressure, component role, and state behavior.
4. Mark fixed, scrollable, sticky, keyboard-avoiding, sheet, dialog, and system-handoff behavior.
5. Map entry, exit, primary action, secondary actions, and interruption recovery.
6. Cover every upstream state; distinguish state changes from new screens.

Use neutral boxes and labels in visual artifacts. A wireframe may specify hierarchy, density, copy length, and interaction intent, but must not pretend to establish final tokens or visual direction.

## Check the core flow

Trace at least one critical before/during/after path and one failure or interruption path. Verify that the primary action remains reachable, content identity survives errors, destructive actions have a consequence boundary, and system surfaces have in-app fallbacks.

Read [references/wireframe-rules.md](references/wireframe-rules.md) before finalizing regions and [references/wireframe-schema.md](references/wireframe-schema.md) before creating JSON.

## Produce and validate

Create:

- `wireframe.md` using [assets/wireframe-template.md](assets/wireframe-template.md).
- `wireframe.json` using [assets/wireframe-template.json](assets/wireframe-template.json).

Run `python3 scripts/validate_wireframe.py <path-to-wireframe.json>` and fix every error. When an upstream UX file is available, also run `python3 scripts/validate_wireframe.py <path-to-wireframe.json> --source-ux <path-to-ux-architecture.json>` to check screen and state coverage.

## Enforce the output order

1. Source contract and assumptions.
2. Navigation and flow skeleton.
3. Screen inventory and region contracts.
4. State, overlay, keyboard, and system-surface behavior.
5. Traceability and unresolved decisions.

Do not finish with a styled mockup disguised as a wireframe or with a screen inventory that omits states and recovery.
