---
name: ui-flow
description: "Improve a complete user journey, including error recovery. Use for a multi-step journey's decisions and recovery; ui-states defines individual screen states."
---

# ui-flow

Improve a complete user journey, including error recovery.

## Choose this workflow

Use for a multi-step journey's decisions and recovery; ui-states defines individual screen states.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [UI and frontend methods](../../references/packs/ui.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; user goal, entry/exit points, current flow, and success constraints.

**Pack prerequisites:** Target screens/flows, existing design conventions, and runnable UI or supplied references. Visual claims require actual renders; accessibility claims distinguish automated, keyboard, and assistive-technology evidence.

- **Infer from evidence:** Inspect the target flow, existing components/tokens, actual renders or supplied references and current responsive behavior.
- **Reasonable default:** Reuse established visual conventions and preserve keyboard behavior; label unrendered changes as visually unverified.
- **Ask only when needed:** Ask about an unresolved interaction or visual direction only when plausible choices materially differ; do not make a missing screenshot block source inspection.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

One complete journey including cancellation, errors, navigation, and recovery.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Walk the journey through entry, progress, validation, abandonment, retry and return paths, mapping decisions and state transitions.
2. Track which user input and permissions survive each transition, and identify dead ends and friction.
3. Propose improvements; ui-states or design implements accepted changes.

## Technical method

- **Inspect:** Map the user's objective, steps, branching choices, saved state and recovery from interruption.
- **Method:** Remove unnecessary decisions while retaining needed confirmation and context; define back, refresh and retry semantics.
- **Avoid misdiagnosis:** Optimizing one screen can break cross-screen state or erase work when users navigate backward.
- **Check the result:** Complete the journey from a fresh start, an interrupted state and a recoverable failure with realistic input methods.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [UI and frontend worked example](../../references/examples/ui.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).
- The affected project uses Flutter: [Flutter](../../references/frameworks/flutter.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves gsap, motion design, framer motion, view transition, click path; load only the matching method: [Motion, visual direction and click paths](../../references/methods/motion-design.md).

## Decision branches

- **When back navigation or session expiry discards important work:** Define recovery and preservation explicitly before simplifying the journey.

## Deliver and verify

- Journey/state map with dead ends, prioritized recovery changes and an acceptance walkthrough.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Users can recover from a mid-flow failure; back navigation does not silently discard required state.

## Stop and recover

- Do not simplify by removing necessary policy or consent steps. Distinguish observed usability issues from assumptions needing user testing.

## Example requests

- **Normal (plan):** Plan improving account recovery, including expired links and back navigation.
- **Edge (plan):** Plan how the onboarding flow recovers when session expiry interrupts it midway through a form.
- **Blocked (inspect):** Assess a flow from mockups without claiming observed conversion improvements.
