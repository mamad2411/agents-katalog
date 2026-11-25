---
name: high-fidelity-prototype
description: Build or refine interactive high-fidelity prototypes for this project, grounding visuals, motion, and interaction in existing components and validating the chosen runtime. Use for prototype deliverables, including native HUDs and panels, rather than routine production implementation.
---

# High Fidelity Prototype

Make a prototype the user can operate and judge at its intended size. Preserve the product's visual and interaction contracts while making simulated behavior explicit.

This skill owns prototype construction and delivery. Repository rules remain authoritative for access, runtime isolation, design synchronization, and validation. Combine with [apple-design](../apple-design/SKILL.md) for Apple interface decisions and [runtime-debugging](../runtime-debugging/SKILL.md) when inspecting the running app. It does not authorize production integration, publication, other conversation access, or delegation.

## Establish the fidelity target

Read the supplied references and relevant implementation before selecting a medium. Carry forward the latest confirmed corrections; an earlier screenshot or abandoned experiment is not the final specification. Distinguish implemented behavior, agreed design decisions, and new proposals.

For an existing surface, map the proposed change to its owning views and controllers, assets and text, state transitions, and input and window behavior before choosing a harness. Identify the existing behavior to preserve and the explicit design delta. Read the composition and presentation chain, not only the geometry, material, or effect helpers.

Trace affected capabilities from entry point through action routing, data or draft ownership, execution, and outcome. Include menus, shortcuts, and drops when the surface exposes them. A reused button with a different callback, an inert drop handler, or several command IDs routed to one scenario does not preserve the original capability. Keep a compact before/proposed/evidence map; mark intentional changes and unimplemented paths explicitly.

When adding a mode or activity, check which existing workflows can coexist with it. Preserve their reachable entry points unless changing them is part of the accepted design. Distinguish launch source, input session, task/run identity, execution capability, and presentation state: several surfaces may show one operation, and a completed service run may still be writing or presenting its result. Trace replacement, cancellation, focus, and handoff rules through their owners before combining state machines.

For the affected flow, establish:

- What must be real to judge it: material, window behavior, component geometry, animation, input, or backend behavior.
- What may be simulated: task progress, model responses, target content, access decisions, or network conditions.
- The entry point, meaningful intermediate states, user actions, outcome, and return to rest.
- The evidence needed to judge the result: interactive artifact, native window, representative captures, or a continuous recording.

Keep this contract proportional to the request. A motion study may need one component and a replay control; it does not automatically need a complete application or every failure scenario.

## Choose the medium that can demonstrate it

| Intended judgment                                                        | Suitable medium                                         | Evidence boundary                                                   |
| ------------------------------------------------------------------------ | ------------------------------------------------------- | ------------------------------------------------------------------- |
| Composition, information hierarchy, or state comparison                  | Figma or a static design artifact, as requested         | Cannot establish runtime behavior                                   |
| Interactive flow, form states, or responsive layout                      | Executable web prototype or the actual renderer         | Browser approximations cannot verify native focus or desktop glass  |
| Real HUD, desktop material, window placement, or cross-application focus | Native prototype or isolated product runtime            | A standalone harness proves only the native pieces it actually uses |
| Service, bridge, permissions, or real execution behavior                 | Isolated product runtime with the required dependencies | Simulated events cannot establish integration correctness           |

Honor an explicit requested format. If it cannot demonstrate a required property, identify that limitation instead of silently replacing the deliverable or claiming equivalence. Read [native-prototypes.md](references/native-prototypes.md) when building an executable macOS surface.

## Reuse the owning components

Inspect the existing surface, shared controls, tokens, assets, and state contracts. Reuse the level that owns the behavior being judged: an icon copied from the product does not make a recreated form or window faithful.

For fidelity to an existing surface, compare running its actual components or package with mocked service boundaries and an isolated full-app run before replacing its presentation or interaction owner. Controller coupling alone does not justify a recreation. Choose the smallest option that preserves the behavior being judged; a focused effect study can still use a small component harness. Keep necessary adapters narrow and their behavioral differences explicit. Avoid refactoring production architecture solely to make a temporary demonstration compile.

Establish a runnable baseline from the unchanged owning source before adding the proposed states. Compare its appearance and interactions at the intended size, then implement only the scoped delta. Derive new states from that owner and the user's design decisions; do not add controls, drag handles, or a permanently expanded presentation just to simplify the harness. For native baseline and interaction checks, follow [native-prototypes.md](references/native-prototypes.md).

Keep prototype sources and build output in a task-owned location under the repository's ignored artifact conventions, or the user's requested destination. When copying source into a stable prototype snapshot, record the repository-relative origins and revision or content hashes; do not silently refresh code already used by another part of the prototype. Preserve attribution and keep private source references out of tracked content.

## Build one coherent interactive flow

Use a shared scenario state for related surfaces so labels, controls, simulated frames, and completion agree. Drive presentation from that state; keep animation clocks separate from task progression. Replaying or resetting should cancel outstanding scenario work so old callbacks cannot change the next run.

Mock external effects at the boundary while retaining the intended action and identity. A simulated screenshot still enters the appropriate draft; a simulated command still uses the selected command and its parameters. Keep independent operations independent and projections of the same operation linked. Do not treat opening a view as taking over execution, hiding a view as cancellation, or a stop request as an acknowledged outcome unless the owning contract says so.

Implement the states needed for the requested experience, with realistic content and actionable controls. For example, a command demonstration may cover input → execution → insertion or verification → completion → dismissal. A monitoring study may also need approval, disconnect, or independent tasks. Do not add these merely to fill a checklist.

Preserve the product's interaction semantics:

- A dispatched operation is not a confirmed outcome. Show stopping or confirmation pending until the scenario's acknowledgement arrives; do not disguise cancellation as pause/resume.
- Keep selected task identity stable when unrelated progress arrives. If multiple tasks are in scope, controls and monitoring must act on the same task, and stopping one must leave the others alone.
- Preserve input drafts and selected values across the intended handoff between surfaces. Verify keyboard submission, input-method composition, dismissal, and focus return when those interactions are part of the prototype.
- Identify simulated monitoring and stale frames clearly. A disconnected or frozen frame must not appear live, and closing a monitor must not silently stop the task.

Place replay, scenario selection, and optional live tuning in a distinct demonstration controller. Use it to adjust parameters that affect the current study without rebuilding. Demo-only appearance overrides and playback controls should not be mistaken for proposed product settings or task controls. Useful tuning controls act on the running surface, provide a reset, and retain the chosen values for repeatable comparison.

## Preserve motion continuity

For an effect that should accompany the surface from its first visible frame, prepare its initial state before presenting the window. Check the combined window, content, and effect timing; nested fades or a late mount can produce visible lag even when individual durations look correct.

Keep a continuous effect mounted across adjacent busy phases when the design calls for continuity. Change phase color or intensity smoothly, retain animation during its exit transition, and stop hidden work once the exit finishes. Avoid tying the effect's identity to changing text or recreating it on every progress event.

Select motion from the agreed reference and current implementation. A color palette, reveal shape, or duration from one experiment is not a universal preset. Verify both the complete flow and direct parameter changes, including rapid reversal where relevant. Respect reduced motion and visibility lifecycle without removing essential state feedback.

## Verify and deliver

Follow the repository's Visual Acceptance sequence: inspect one representative composition before expanding it, then exercise the actual controls and affected transitions. Compare the result with the unchanged baseline for hierarchy and behavior as well as styling, accounting for the requested delta. Match checks to the claim—compilation, screenshots, interaction checks, and native composition each establish different facts. Inspect motion at normal speed and use early or intermediate frames when timing is the issue.

For integrations, exercise the existing workflow while the added activity is present, not only each flow in isolation. Choose the meaningful intersections: an open draft receiving unrelated progress, another launch during execution, the same run shown in two places, or a user action during result delivery. Check the capability map against actual action outcomes; visual reuse and isolated scenario checks cannot establish functional integration.

Deliver the usable artifact with its source location and concise launch/replay instructions. Distinguish actual source reuse, adapted or recreated behavior, and simulated data or execution; state what was verified and any material gap. Keep the prototype reproducible; do not delete the deliverable while cleaning up temporary runtime data. Stop only task-owned verification instances, and distinguish those from a preview intentionally left open for the user.
