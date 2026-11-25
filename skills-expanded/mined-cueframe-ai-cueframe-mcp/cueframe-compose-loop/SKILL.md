---
name: cueframe-compose-loop
description: "Use when previewing, reviewing or revising a CueFrame composition, including a scoped correction, reference comparison or final-delivery check. Also use when an agent should drive CueFrame to a high-quality clip itself: author, look at rendered frames, score with the judge, fix the weakest thing and repeat, over the primitives in the `cueframe-cli` skill. Triggers on \"turn this source into a polished 9:16 clip\" or \"compose and self-correct until it scores well\"."
---

# CueFrame preview and revision

Use the [project and capability policy](../composing-video/references/project-policy.md). This skill owns evidence, revision scope and delivery; craft and format skills describe what to look for.

Read the current saved composition and relevant source before changing it. Reuse the approved brief or supplied reference. A local correction does not restart planning. On a resumed or delegated turn, recover the full goal, the distinct scoped amendment and the current saved review state from the existing brief, ledger or notes; inspect the relevant evidence before continuing. For exact builtin preset/recipe insertion, use [builtin insertion](references/builtin-insertion.md).

## Inspect the behavior that matters

Read [preview workflow](references/preview-workflow.md) to choose the supported hosted or local surface. Match evidence to the question: stills for typography/geometry, motion for paths and handoffs, audio inspection for the mix. Requested timestamps, artifact URLs and successful jobs are not proof that their content was observed.

Locate a finding in the film: when it happens, what is visible or audible, what the brief/reference requires, and which relationship needs to change. For reconstruction, compare matching source/output landmarks and the interval between them. If a requested revision deliberately changed timing, compare corresponding events rather than pretending they still share timestamps.

For a card or title covered by media, inspect the saved [visual track order](../composing-video/references/tool-map.md#visual-track-order) before changing its HTML or typography.

Fix the highest-impact cause you can explain. A layout failure may need a grid change, a position adjustment, a different parent transform or a new shot choice. Do not force every correction into one technique. Use targeted atomic operations against the observed revision and retain concurrent edits. Every committing batch needs the required `if_match` from the current read. After a conflict, reread the changed state and rebuild the intended change; never resend old operations with the error's `currentEtag`.

## Recheck the affected scene

A timing change can affect more than the edited clip: backing plates, screen masks, linked controls, captions, sound and neighboring handoffs. Inspect the changed window with its entrance/exit context. If the ending must be preserved, verify the complete final scene through its last frame, not just an unchanged logo object. Check saved values as well as actual output. Review verdicts cover only the inspected windows and identified composition/source versions. Retain unaffected review results; recheck affected windows when their source or version changes.

Return a failed saved comparison to the same author, or an explicit successor with the goal, amendment, saved state and evidence intact. Saving source changes alone leaves review unfinished. Do not report a repair complete until its saved output has been reinspected; see [handoff and review continuity](../cueframe-reference-video/references/measurement-and-comparison.md#handoff-and-review-continuity).

`score_composition` can supply broader editorial, spatial, brand and caption critique when useful and within budget. Its fixed caption criterion can penalize intentionally uncaptioned work; do not add captions solely to improve a score. These instructions do not change judge behavior. A failed brief requirement remains a failure regardless of a numerical score.

Continue while evidence suggests a useful correction within the task's time/cost scope. If progress stalls, change the diagnosed cause or report the remaining gap; repeated scores alone are not progress. A scoped edit can finish with verified previews. For a finished-video request, export the saved revision and inspect the resulting artifact. Report the output, what was actually reviewed, and unresolved limitations.

## Detailed guidance

[The convergence loop](references/convergence-loop.md) has the step-by-step author, preview, score, fix and stop procedure for an agent driving a clip to quality.
