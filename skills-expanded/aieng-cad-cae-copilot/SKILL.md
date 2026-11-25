---
name: aieng-cad-cae-copilot
description: MCP-first evidence workflow for AIENG CAD/CAE setup, solver preflight, approval-gated solver execution, and result extraction. Use when the user asks to inspect CAE readiness, patch setup, prepare/run CalculiX, or report stress/displacement evidence.
---

# aieng-cad-cae-copilot

MCP-first CAE workflow discipline for agents operating the active AIENG Workbench.
This skill teaches order of operations and claim discipline; it does not add solver capability.

## Purpose

- Use package evidence and MCP tool returns as the source of truth.
- Prepare solver runs without inventing missing material, loads, or constraints.
- Keep `cae.run_solver` behind the approval boundary.
- Report only evidence-backed results and explicit limitations.
- For repeatable loops, follow the relevant entry in
  `../engineering_skill_contracts.json`: `cae-preflight`,
  `solver-run-orchestrate`, `design-target-review`, or
  `evidence-report-synthesize`.

## When to use

Use for CAE readiness inspection, setup patching, solver preflight/deck generation, solver execution, FRD metric extraction, field-region extraction, and refreshed result summaries.
Do not use for new CAD authoring or schema/tool implementation.

## Required workflow

1. Inspect state with `aieng.agent_context { project_id }` and, when needed, `aieng.inspect_package` or `aieng.write_completeness_report`.
2. If material, loads, or constraints are missing, ask the user or apply explicit setup with `cae.apply_setup_patch`.
3. Run `cae.prepare_solver_run { project_id }` before any solver execution. Use the `recommended_next_calls` list in the response to decide the next `cae.*` call.
4. If the input deck is missing but setup is sufficient, call `cae.generate_solver_input { project_id }`.
5. Call `cae.run_solver { project_id }` only after successful preflight and only through approval. If `AIENG_MCP_BLOCK_APPROVAL_TOOLS=1` is active, report the server refusal and stop.
6. After a successful solver run, call `cae.extract_solver_results`, optionally `cae.extract_field_regions`, then `postprocess.refresh_cae_summary`.
7. Re-read context/results before reporting final numbers.

## Credibility tiering

Every result-bearing output carries a single `credibility` stamp (the shared
V&V-40 tier). Ordered low → high: `critique_finding` < `surrogate_prediction` <
`proxy_assembly_result` < `executed_solver_result`. Read `credibility.tier` and
report it with the numbers; never present a lower tier as if it were an
executed-solver result. An output that claims a solver result without
`solver_executed: true` is downgraded to `unverified` (rank 0) with a
`downgrade_reason` — treat it as not solver-backed. `production_ready` is `false`
unless explicitly certified.

## Hard rules

- Never claim a solver ran unless `cae.run_solver` completed successfully and result artifacts exist.
- Surface the `credibility` tier of any result you report; do not upgrade a proxy/surrogate/critique result to "verified".
- Never claim convergence unless solver evidence supports it.
- Treat stale artifacts as historical until refreshed or rerun.
- FRD scalar extraction is not full field validation.
- AIENG package readiness is not physical certification.
- Respect all `[APPROVAL REQUIRED]` tools and user decisions.

## Response contract

Report: current evidence state, setup changes, preflight result, approval status, solver/result artifacts, extracted metrics, stale evidence, and limitations.
