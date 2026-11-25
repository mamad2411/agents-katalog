---
name: motion-build-inspect-repair
description: Build a requested animated webpage or interface, inspect its actual running motion, diagnose observed defects, apply authorized source repairs and verify the same interaction again. Use for end-to-end prompt-to-page delivery with Motion Debugger's recorded frames and temporal evidence, including 3D UI.
---

# Prompt → build → inspect → repair

Own the requested interface through an evidenced result. The host coding agent builds and edits source; this plugin supplies design guidance and local observation tools. An MCP configuration entry alone does not prove the tools are connected.

## Follow the bounded workflow

Use distinct stages: brief → design → build → inspect → repair 1 → verify 1 → repair 2 → verify 2 → report. A passing inspection or verification can go straight to report. An exact permission, environment or evidence blocker goes to a blocked report. Every stage is visited at most once; a second attempt is a new numbered node, not a back edge.

Allow at most two evidence-led source repair attempts within this plan. After verify 2, report any unresolved failure with evidence rather than silently starting another iteration. Repairs already inside the user’s build/fix request remain autonomous. Do not treat missing evidence as success. The plugin also ships the machine-readable graph and validator under `workflows/`; this is a host-agent plan, not a hidden execution engine.

## Build the requested product

Read the brief, repository instructions and existing package setup. Write down the primary interaction, the intended visual result and important final state. Use the `motion` router and `motion_recipe` for concrete interactive patterns, `motion-design` for the page and `motion-3d-ui` when real spatial motion is needed. Preserve the user's requested stack and task; do not replace a difficult requirement with a different demo.

Implement the first usable version, then run a cheap native-browser functional check before investigating motion. Define and execute the primary input → positive result journey with a bounded deadline and an explicit visible-error check. A stable rectangle, a finished recording, equivalent endpoints or zero uncaught errors does not prove task completion: the app can catch an exception and remain stuck. Exercise actual browser timers and other browser APIs, not only mocks or Node tests. Fix a broken primary control before lower-priority easing. Keep time for verification within the total budget and preserve the last working source checkpoint.

If motion tools cannot connect or Chromium cannot launch, report that blocker; ordinary screenshots or static tests may still help, but do not label them recorded motion proof.

## Observe before diagnosing

Choose the real loopback URL, a unique target and an authorized, repeatable interaction. Capture ordinary use plus a revealing interruption or reversal when applicable. Fix the recipe, viewport, reduced-motion setting, duration and meaningful expectations before comparing a repair.

Choose duration and frame times from the whole intended interaction, including delayed completion and interruption, rather than relying on default duration or the first metric finding. Use an ordinary browser check for a journey that exceeds the tool's bounds; do not shorten the success criterion to fit. Inspect page-level desktop/narrow composition as well as target motion. During a narrow repair, preserve the approved layout, copy, assets and features unless the observed defect requires changing them.

For a temporal investigation, call the actual MCP tools in this sequence:

1. `motion_capture({recipe})`: record the running interaction and keep its capture ID
2. `motion_inspect({captureId, fromMs, toMs, includeSamples:true})`: inspect a bounded window near the reported finding; use events and sample cadence to distinguish an app jump from weak sampling
3. `motion_frames({captureId, selection:"journey", maxWidth:1280, maxHeight:960})`: consume the returned native PNG images spanning the whole capture. Then request `timestampsMs` around an interruption or defect for detailed review. Inspect more than endpoints. Seeking is approximate; the trace is the timing authority

If a wrapper exposes images only as base64 or local PNG paths, decode/view the actual images with available image tools. Receiving frame metadata is not the same as looking at the frame. Raw evidence is available at `motion-evidence://capture/<captureId>`.

Treat functional journeys as ordered requirements. For a removal flow, remove the item, activate the visible Undo control while its toast is still available, and verify that the item and its prior quantity are restored. Verify ordinary pointer activation separately from keyboard focus/activation; success with Enter does not prove the control accepts a click. A nonzero rectangle, opacity and computed visibility establish rendered geometry, not clickability: overlays, hit testing, `pointer-events`, disabled state or occlusion can still block the interaction. Use actual unforced input and retain its failures.

If `motion_capture` returns an error with `status: incomplete`, inspect its capture ID and recorded frames as evidence of the failed action. This report is discoverable through list/inspect/resources, but its incomplete trace and unmeasured final state cannot establish a passing contract or a completed before/after comparison. Repair the supported interaction failure, then rerun the same functional journey within the two-attempt bound. Privacy/security rejections intentionally retain no pixels.

Choose only contracts that express the intended design. Frame/height/containment budgets are caller expectations, not universal quality scores. Use final-state expectations so a visually stable “repair” cannot simply disable the interaction. For canvas/3D, video-derived frames show internal scene motion; DOM rectangle metrics alone do not. Marked scene state and source references are annotations, not independently inferred causes.

## Diagnose and repair from evidence

Connect a visible or measured failure to a specific code path. State the observation, a candidate cause and a test that could distinguish it from alternatives. Inspect the relevant source through the normal coding tools. Do not infer a defect from an animation cancellation alone, and do not copy a reference branch or a prewritten “fixed” implementation as the answer.

When source repair is within the user's requested build/fix scope, apply the smallest justified change and continue without an unnecessary approval roundtrip. This skill does not authorize unrelated installs, production changes, credentials or external publication. If the evidence is inconclusive, narrow the reproduction and observe again instead of rewriting the whole animation.

Repeat the original `motion_capture` recipe after the change, then call `motion_compare({beforeId, afterId})`. Inspect the after frames as well as metrics. A comparable result, intended final state and a visibly correct transition are all useful; one passing assertion is not a complete review. Do not raise a failing budget merely to manufacture a pass or remove the feature being tested.

If verify 1 still shows a justified defect, continue to repair 2 and verify 2. After that, stop with the unresolved report if a defect remains. Preserve capture IDs across attempts so a later improvement cannot erase the original evidence. Stop when the requested interaction is visibly correct and its meaningful contracts/tests pass, or when a concrete permission/environment blocker prevents further work. Report unresolved limits plainly.

## Deliver the product and proof

Give the running preview/artifact, the principal behavior, changes made from the observed evidence, before/after IDs or links and remaining limits. Include desktop/narrow viewport and reduced-motion checks when relevant. Distinguish an agent-written repair from a handwritten reference branch, and a single run from evidence of general agent improvement.

Report functional completion, visual review and temporal evidence separately, each as passed, failed or unverified with its evidence. Missing outcome evidence cannot become a successful delivery; a motion-contract pass cannot override a failed journey or a visibly worse composition.
