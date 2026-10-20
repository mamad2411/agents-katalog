---
name: ui-visual-diff
description: "Compare screenshots against an accepted reference. Use to compare matched visual states; match closes gaps against an accepted reference, and ui-audit judges usability of the resulting interface."
---

# ui-visual-diff

Compare screenshots against an accepted reference.

## Choose this workflow

Use to compare matched visual states; match closes gaps against an accepted reference, and ui-audit judges usability of the resulting interface.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [UI and frontend methods](../../references/packs/ui.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect existing captures; reference/current renders with matching viewport, state, data, fonts, and theme.

**Pack prerequisites:** Target screens/flows, existing design conventions, and runnable UI or supplied references. Visual claims require actual renders; accessibility claims distinguish automated, keyboard, and assistive-technology evidence.

- **Infer from evidence:** Inspect the target flow, existing components/tokens, actual renders or supplied references and current responsive behavior.
- **Reasonable default:** Reuse established visual conventions and preserve keyboard behavior; label unrendered changes as visually unverified.
- **Ask only when needed:** Ask about an unresolved interaction or visual direction only when plausible choices materially differ; do not make a missing screenshot block source inspection.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Visual differences and regression classification; match applies visual fixes.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Match viewport, DPR, fonts, content, theme and animation state across the captures.
2. Mask only justified nondeterminism, identify the meaningful changed regions and describe differences by user impact.
3. Inspect changed regions before accepting any baseline.

## Technical method

- **Inspect:** Record baseline approval, viewport, fonts, data, time and screenshot environment.
- **Method:** Compare matched states, separating rendering noise from layout/content changes; inspect differences before replacing a baseline.
- **Avoid misdiagnosis:** Approving a new screenshot merely because it differs converts a regression into the expected result.
- **Check the result:** Reproduce significant differences with stable fonts/data and retain both images plus a reason for accepted changes.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [UI and frontend worked example](../../references/examples/ui.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).
- The affected project uses Flutter: [Flutter](../../references/frameworks/flutter.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves gsap, motion design, framer motion, view transition, click path; load only the matching method: [Motion, visual direction and click paths](../../references/methods/motion-design.md).

## Decision branches

- **When captures differ in environment or content:** Recreate comparable captures or give qualitative differences without a precise pixel claim.

## Deliver and verify

- Annotated difference report with capture conditions, changed regions, accepted differences with reasons, remaining mismatches and confidence.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A layout shift is detected; a timestamp-only change is not misclassified as a design regression.

## Stop and recover

- Capturing a local build is bounded local execution; capturing a shared or remote target needs that target in scope. Unmatched conditions invalidate precise pixel-difference claims.

## Example requests

- **Normal (inspect):** Compare these matched-viewport screenshots and separate dynamic noise from regressions.
- **Edge (inspect):** Compare screenshots with dynamic timestamps and a real layout shift.
- **Blocked (inspect):** Compare supplied captures with unknown font loading; do not assert exact pixel fidelity.
