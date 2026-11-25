---
skillx:
  name: casadi-ipopt-nlp
  purpose: Formulate and solve the full nonlinear AC OPF with CasADi+IPOPT, then emit a complete report artifact aligned with solved physics and task schema expectations.
  scope_in:
    - decision-variable construction for AC OPF state and dispatch
    - nonlinear objective and feasibility-constraint assembly
    - solver execution, initialization strategy, and solution extraction
    - report shaping from solver-backed values
  scope_out:
    - not for replacing AC constraints with DC or simplified surrogates
    - not for fabricating feasible-looking outputs from failed solves
    - not for redefining parser-owned data semantics
  requires:
    - parsed network artifact with consistent per-unit scaling
    - branch-physics artifact with exact bidirectional equations/limits
    - explicit variable and constraint bounds
  preferred_tools:
    - casadi
    - IPOPT
    - deterministic residual and bound checks before report emission
  risks:
    - hidden infeasibility from sign/unit mismatch upstream
    - weak initialization causing false-negative solver failures
    - schema-complete report generated from physically inconsistent values
    - aggressive rounding causing verifier threshold violations
  examples:
    - input: Solve AC OPF and write final report.json for benchmark verification.
      expected_behavior: run honest NLP solve, preserve feasibility evidence, and export numerically consistent fields.
---

# Stage Contract

## Input Artifact
- `network_parsed` (data stage)
- `branch_model_contract` / equations (branch stage)
- task-required report schema definition (from task materials)

## Output Artifact
- `opf_solution_state`:
  - solver termination fields (status/success diagnostics)
  - primal vectors (`Vm`, `Va`, `Pg`, `Qg`, and other modeled variables)
  - objective value and core feasibility metrics
- `report.json` candidate:
  - complete task-required schema
  - values sourced from solved state, not placeholders

## Handoff Rule to Final Output
- Emit `report.json` only when schema completeness and feasibility checks both pass.
- If solve fails or is infeasible, report failure transparently with diagnostics; do not claim feasibility.

# Execution Guidance

1. Define AC OPF variables with strict ordering and matching bound vectors.
2. Assemble objective and constraints using upstream branch equations and correct unit conventions.
3. Enforce reference-angle and network feasibility constraints explicitly.
4. Run IPOPT with stable options and at least one fallback initialization strategy.
5. Extract solution vectors deterministically and map them to report fields.
6. Apply precision discipline (no premature coarse rounding).

# Deterministic Pre-Report Checks (Required)

- Solver evidence:
  - termination status captured and exposed
  - no silent exception-swallowing path that emits success output
- Constraint quality:
  - equality residuals and inequality violations within configured tolerance
  - variable values within bounds (with tolerance)
- Physical consistency:
  - nodal balance terms align with branch-flow formulation and sign conventions
  - branch thermal checks use bidirectional apparent power limits
- Report completeness:
  - all required schema fields present
  - every numeric field derived from solved variables/derived checks

# Common Failure Modes

- Reporting “solved” when IPOPT returns non-success status.
- Mixing MW and per-unit inside objective/constraints.
- Omitting feasibility diagnostics while still emitting polished JSON.
- Recomputing report values with inconsistent formulas vs optimization constraints.