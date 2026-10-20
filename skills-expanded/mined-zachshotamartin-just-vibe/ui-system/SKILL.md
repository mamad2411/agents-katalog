---
name: ui-system
description: "Establish typography, spacing, colors, tokens, and component conventions. Use to establish or refine shared design tokens/components; polish makes local refinements and build implements an accepted adoption."
---

# ui-system

Establish typography, spacing, colors, tokens, and component conventions.

## Choose this workflow

Use to establish or refine shared design tokens/components; polish makes local refinements and build implements an accepted adoption.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [UI and frontend methods](../../references/packs/ui.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; existing screens, brand constraints, reusable components, and desired consistency.

**Pack prerequisites:** Target screens/flows, existing design conventions, and runnable UI or supplied references. Visual claims require actual renders; accessibility claims distinguish automated, keyboard, and assistive-technology evidence.

- **Infer from evidence:** Inspect the target flow, existing components/tokens, actual renders or supplied references and current responsive behavior.
- **Reasonable default:** Reuse established visual conventions and preserve keyboard behavior; label unrendered changes as visually unverified.
- **Ask only when needed:** Ask about an unresolved interaction or visual direction only when plausible choices materially differ; do not make a missing screenshot block source inspection.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Tokens and component conventions; implementing an adoption is a separate build or polish request.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Inventory actual repeated values and component states.
2. Define semantic token roles over a small coherent raw scale, and the component states they cover.
3. Plan incremental adoption with representative specimens that show no visual regressions.

## Technical method

- **Inspect:** Inventory repeated tokens, typography, spacing, component states and existing theme contracts.
- **Method:** Define semantic roles and a small consistent scale; migrate consumers incrementally with deliberate exceptions.
- **Avoid misdiagnosis:** Renaming colors without updating focus, disabled, dark-mode or data-visualization states leaves an incomplete system.
- **Check the result:** Render representative components in each supported theme and verify contrast, overflow and token fallback behavior.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [UI and frontend worked example](../../references/examples/ui.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).
- The affected project uses Flutter: [Flutter](../../references/frameworks/flutter.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves gsap, motion design, framer motion, view transition, click path; load only the matching method: [Motion, visual direction and click paths](../../references/methods/motion-design.md).

## Decision branches

- **When two themes require different contrast relationships:** Map semantic tokens per theme and verify components rather than applying one global color substitution.

## Deliver and verify

- Token roles and scales for typography, spacing, color and state, a component state matrix, and a migration mapping with examples.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Tokens express meaning across components; contrast and long-content behavior remain usable in representative states.

## Stop and recover

- Do not replace branding or add a component framework without need. Resolve competing theme requirements explicitly.

## Example requests

- **Normal (plan):** Plan semantic design tokens from the existing screens and brand constraints.
- **Edge (plan):** Plan consolidating spacing and color tokens across light and dark settings screens.
- **Blocked (inspect):** Plan a system from existing UI without replacing unavailable brand assets.
