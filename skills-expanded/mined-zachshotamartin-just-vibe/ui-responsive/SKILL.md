---
name: ui-responsive
description: "Fix layouts across screen sizes and input methods. Use for layout adaptation, zoom and input differences; responsive is the same canonical workflow."
---

# ui-responsive

Fix layouts across screen sizes and input methods.

## Choose this workflow

Use for layout adaptation, zoom and input differences; responsive is the same canonical workflow.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [UI and frontend methods](../../references/packs/ui.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; target layouts, content extremes, and supported input/viewport conditions.

**Pack prerequisites:** Target screens/flows, existing design conventions, and runnable UI or supplied references. Visual claims require actual renders; accessibility claims distinguish automated, keyboard, and assistive-technology evidence.

- **Infer from evidence:** Inspect the target flow, existing components/tokens, actual renders or supplied references and current responsive behavior.
- **Reasonable default:** Reuse established visual conventions and preserve keyboard behavior; label unrendered changes as visually unverified.
- **Ask only when needed:** Ask about an unresolved interaction or visual direction only when plausible choices materially differ; do not make a missing screenshot block source inspection.

Declared evidence requirements: `project.read`, `browser.inspect`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Layout adaptation including touch, pointer, zoom, and keyboard effects.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Reproduce the failure and inspect intrinsic sizes and flow to find the width constraint or overflow source.
2. Adjust the layout at content-driven boundaries.
3. Test nearby and intermediate widths, long text, keyboard focus and relevant orientation changes.

## Technical method

- **Inspect:** Inspect layout constraints, intrinsic content size, breakpoints, zoom, touch targets and input methods.
- **Method:** Repair the constraint causing overflow; choose reflow/order based on task meaning rather than arbitrary device names.
- **Avoid misdiagnosis:** Hiding overflow can conceal controls; hover-only affordances fail on touch or keyboard.
- **Check the result:** When no product matrix exists, test at least 320 CSS px width without two-dimensional scrolling (256 px height for vertical scrollers, WCAG 1.4.10), 200% text resize (1.4.4), increased text spacing (1.4.12), both orientations (1.3.4) and 24 by 24 CSS px targets or equivalent spacing (2.5.8); essential content and pointer/keyboard access must remain unclipped.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [UI and frontend worked example](../../references/examples/ui.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).
- The affected project uses Flutter: [Flutter](../../references/frameworks/flutter.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves gsap, motion design, framer motion, view transition, click path; load only the matching method: [Motion, visual direction and click paths](../../references/methods/motion-design.md).

## Decision branches

- **When hiding an element would remove required functionality:** Reflow or provide an equivalent reachable interaction instead of suppressing it.

## Deliver and verify

- Layout fixes with a viewport/content/input matrix and observed reachability and overflow results.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Content remains reachable at narrow widths and zoom; hover-only controls have a usable alternate interaction.

## Stop and recover

- Do not hide required functionality or claim device coverage from a single desktop screenshot.

## Example requests

- **Normal (apply):** Fix the checkout layout for narrow screens, zoom, and touch input.
- **Edge (apply):** Repair a table at narrow widths and high zoom without hiding essential actions.
- **Blocked (inspect):** Review responsive source and screenshots without claiming real-device interaction coverage.
