---
name: review-conformance
description: Conformance review — verify Codex's output against the confirmed requirements, the approved plan/architecture, and the task's acceptance criteria before any quality nitpicking.
---

# Conformance Review (first pass, before quality)

Wrong-but-clean code is worse than ugly-but-right code. Check conformance FIRST.

## Three-level check

1. **Requirement conformance** — For each acceptance criterion of the task: point at the exact code/test that satisfies it. No pointer = finding. Check scope both ways: nothing promised is missing, and nothing out-of-scope was touched (the `diff.status` list shows every file — files outside the task's declared `Files:` list need justification).
2. **Plan/architecture conformance** — Does the implementation follow the approved design: same components, same data flow, same chosen option? Check the code against PLAN.md's **Contracts** — signatures, data shapes, and API/event contracts must match what was agreed, because other tasks were sliced and reviewed assuming them; a silently changed contract breaks callers this task can't see. Codex substituting its own design is a finding even when it works — the plan was reviewed, the substitute wasn't. If the deviation is genuinely better, surface it to the user as a plan change, don't wave it through.
3. **Structure conformance** — Files in the right places, naming matching conventions, integration through existing seams (not parallel copies of existing helpers), tests where the project keeps tests.

## Evidence rules

- Check the tool result's `status` field first: only review a `success` run normally. A `partial`
  run (no completion marker / parse errors) means the result may be incomplete — verify everything
  from the diff and your own check runs, or re-run the task (see `review-feedback`).
- When the run carried a `verifyCommand`, read the `verification` field before anything else:
  `passed: true` proves the acceptance command exited 0 in the workspace; `passed: false` or
  `skipped` is an automatic unmet criterion — quote its `outputTail` in the finding.
- Work from the tool result's `diff` field (status + patch); read full files when the patch lacks context. Never review from Codex's `agentMessage` alone — it describes intent, not reality.
- Do not re-run the suite per task: read `accepted` and `verification` (the server-run `verifyCommand`) as the acceptance evidence, and run a manual probe only when the acceptance is not a command. `commands` in the result shows what Codex ran and exit codes — confirm the targeted tests plus build/typecheck ran green; Codex is not expected to run the full suite (it runs once per merged parallel wave and once in the whole-feature review).

## Non-code deliverable tasks

For content tasks (built under `codex-flow:exec-deliverable`), conformance = every acceptance
criterion met, the requested format/length honored, and the project's voice/template followed.
Additionally spot-check reproducibility: recompute at least one figure from the source data and
verify at least one external claim against its cited source — fabricated numbers or sources are the
non-code equivalent of a failing test.

## Output

A conformance verdict per acceptance criterion (met / not met / partially met + evidence), feeding into review-feedback for anything not met.
