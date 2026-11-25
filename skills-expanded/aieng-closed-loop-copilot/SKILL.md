---
name: aieng-closed-loop-copilot
description: MCP-first closed-loop CAD/CAE copilot skill for improving an existing solved design against explicit targets. Use when the user asks for bounded design iteration using editable CAD parameters, solver reruns, and evidence-backed comparison.
---

# aieng-closed-loop-copilot

MCP-first closed-loop discipline for recommend → edit → re-simulate → compare.
Use this only when a baseline project has CAD, CAE setup/results, and explicit design targets or user-stated metrics.

## Purpose

- Bound design iteration before changing geometry.
- Prefer safe parameter edits over full regeneration when editable parameters exist.
- Re-run CAE before claiming improvement.
- Stop on target met, no evidence, approval denial, or budget exhaustion.
- For repeatable loops, follow the relevant entry in
  `../engineering_skill_contracts.json`: `cad-mod-propose-verify`,
  `solver-run-orchestrate`, `design-target-review`, or
  `evidence-report-synthesize`.

## Required workflow

1. Define the target, metric, and iteration budget (default: 3).
2. Inspect baseline with `aieng.agent_context`, `aieng.inspect_package`, and result/design-target summaries when present.
3. Discover editable dimensions with `cad.list_editable_parameters` and inspect local/global scope.
4. Choose one change per iteration. Prefer `cad.edit_parameter`; use `cad.execute_build123d`, `cad.replace_part`, or `cad.remove_part` only when geometry must change structurally.
5. After CAD mutation, inspect `regression_diff` (topology drift) and `critique_diff` (a `fail`/`warn` verdict means the edit worsened manufacturability) and refresh semantics if needed.
6. Run `cad.critique` for engineering parts before CAE claims.
7. Prepare CAE with `cae.prepare_solver_run`, generate deck with `cae.generate_solver_input` if needed, then call `cae.run_solver` only through approval.
8. Extract metrics with `cae.extract_solver_results`, optionally `cae.extract_field_regions`, and refresh summaries before comparing.

## Hard rules

- Respect `[APPROVAL REQUIRED]` tools; if `AIENG_MCP_BLOCK_APPROVAL_TOOLS=1` blocks mutation/solver execution, report the block and stop.
- Do not chain multiple CAD changes before re-simulation unless the user explicitly accepts the loss of attribution.
- Do not claim improvement until post-change solver/result evidence exists.
- Read the `credibility` tier on every result: `executed_solver_result` outranks `proxy_assembly_result` outranks `surrogate_prediction` outranks `critique_finding`. Compare like-for-like and never present a lower tier as solver-verified.
- Surrogate proposals are advisory, not evidence: never report a predicted number without its envelope — each prediction carries `uncertainty_std` / `predicted_score_band`, and the proposal set carries a leave-one-out `validation` error band. They guide search only and never substitute for a solver rerun.
- A critique pass or parameter range check is not production certification.
- Stop if target is already met, no safe editable variable exists, no solver evidence can be produced, approval is denied, or budget is exhausted.

## Response contract

Report: baseline evidence, chosen change and reason, approval status, post-change CAD/CAE evidence, metric comparison, termination reason, and limitations.
