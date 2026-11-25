---
name: motion-evidence
description: Capture and compare temporal browser motion evidence on an explicitly requested local application. Use for interrupted reveals, responsive layout jumps, pointer-following continuity, animated drawers and bounded child motion.
---

# Motion evidence workflow

Use the motion-debugger MCP tools, not final screenshots alone, when the bug is temporal.

1. Confirm the caller's local URL, unique target selector and authorized interaction recipe. A capture runs clicks/hover/keys/pointer moves and can change app state. Do not enter credentials, click destructive or payment actions, or load unrelated targets.
2. Define explicit expectations: per-frame position/height budget, visible containment, identity or cancellation budget only if the intended design requires it, and a final interaction-state contract. Bind actual internal DOM/SVG actors when requested. Orientation uses wrapped radians with complete finite phase coverage; anchors use separate same-frame browser reads for both actors. Map plan beats to concrete action indexes with versioned recipe `intent`, and mark destinations terminal or waypoint with their hold action. These are design-specific constraints, not generic quality scores.
3. Set `contract.targetPresence: 'may-disappear'` only if the intended recipe mounts/unmounts or hides the target. Default `continuous` retains the finite-target start/end requirement. Inspect `coverage.intervals` to distinguish observed absence/hidden state from unsampled recorder time. The 80ms integrity gate remains mandatory, even if a caller asks for a larger gap budget.
4. Call `motion_capture` for the before version. It returns compact metrics, failing contracts, candidate event/sample windows and local artifact paths.
5. Use `motion_inspect` with a bounded time window around a finding, then call `motion_frames` with the capture ID. It returns native images decoded from the saved video near a failing window; optionally select up to six capture-relative timestamps. Video seeking is approximate, so use rAF samples for precise measurements. For full raw evidence read `motion-evidence://capture/<id>`.
6. Explain what is browser-observed versus explicitly app-marked/source-mapped. Cancellation can be intentional retargeting; do not diagnose a defect from cancellation alone. A source annotation is not automatically inferred causality.
7. Apply a narrow fix through the coding tools and permissions already authorized by the user. This plugin never edits source itself.
8. Capture after with the same recipe/contracts and call `motion_compare`. Verify intended final state still matches. Report precise contract deltas, evidence paths and remaining limits. `inconclusive` assertions are not passes: lack of an observed violation in an undersampled span does not establish motion quality. Annotation-only, unsupported, reused-anchor and incomplete-phase evidence also remain unverified. Samples never bridge hidden/absent spans or different node identities. Compare the environment/probe/analyzer hashes; diagnose software rendering, long tasks, probe-read cost and superseded tasks before attempting one bounded repeat, and retain every failed attempt.

Optional app annotations use CustomEvent `motion:mark` with `type`, `label`, `sourceKey` and scalar `state`. Optional source mappings require the server owner's explicit MOTION_SOURCE_ROOTS. Do not ask for tokens or persistent access.

If the browser cannot launch, report the blocker and run in a supported environment; never substitute synthetic evidence. Detector ablation is not a benchmark of coding-agent or LLM quality.

For a local 3D app, run a short recorder/environment preflight before spending repair time. Use a production preview so blocked HMR WebSockets do not contaminate capture integrity. If the headless report identifies software rendering and weak sampling on a machine with a desktop, the host may explicitly set `MOTION_BROWSER_MODE=headed` to use a fresh visible local browser. Run `doctor`, inspect its mode/renderer, and freeze that mode for all before/after captures. This does not attach to the user's personal browser profile. Keep the failed trace; do not mix headless and visible captures, loosen the 80ms gate, or turn an environment limitation into an app defect. User-browser screenshots remain separate observations.

For a finished product workflow, exercise every visible action before claiming completion, including undo toasts, keyboard reopening, quantity changes and reduced-motion mode. Check that controls outside a dialog remain reachable and accept pointer input. Record tool timeouts as failures; do not replace them with successful-looking recordings.

Visible geometry is not clickability. A control can have nonzero bounds and opacity yet reject pointer input because of `pointer-events`, an overlay, disabled state or hit testing. Use unforced pointer input, and test keyboard operation separately. For removal and Undo, activate Undo while available and verify restoration of the item and its prior quantity; do not skip a failed Undo or merely wait until the toast disappears.

An interaction error may return `status: incomplete` with a capture ID, failed action index/type/selector/elapsed time and evidence paths. Inspect and view those retained prior events/frames to diagnose the obstacle. The recipe did not complete, final state was not measured, and contracts/comparison cannot pass. Privacy/security rejections purge screenshots and recordings. Apply at most two evidence-led source repairs under the bounded build/inspect/repair workflow.

`maxStepAt60HzPx` expresses interval-average velocity-normalized displacement (observed displacement divided by its associated frame interval, scaled to 60 Hz). It is a caller-defined motion budget, not a universal discontinuity or smoothness score. Preserve the existing math and independent cadence/coverage gates when interpreting it.
