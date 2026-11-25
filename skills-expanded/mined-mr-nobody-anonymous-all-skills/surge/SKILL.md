---
name: surge
description: "Use this skill for transmission power-system studies — AC/DC power flow, DC-OPF / AC-OPF / SCOPF, N-1 / N-2 contingency analysis, PTDF / LODF / OTDF sensitivities, NERC and AC Available Transfer Capability (ATC), SCED economic dispatch, and SCUC unit commitment. Also use for building or editing a tr"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-tool/skills/surge/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Surge workflow

Start by loading a network with `load_builtin_case`, `load_network`, or `create_empty_network`. Solve the base case before any advanced study — contingency, sensitivity, and OPF results are meaningless on a non-convergent base.

## Default tool ladder
1. `load_builtin_case(name)` (e.g. `case118`), `load_network(file_path, format?)`, or `create_empty_network(...)`.
2. `get_network_info()` for counts, totals, areas, zones, voltage levels. `get_topology(...)` / `get_islands()` / `find_path(...)` for connectivity reasoning.
3. `run_ac_power_flow(...)` for the base operating point. `run_dc_power_flow(...)` only when a linearized study is explicitly requested.
4. Sensitivities: `compute_ptdf`, `compute_lodf`, `compute_otdf` for screening and transfer analysis.
5. `run_n1_branch_contingency` / `run_n1_generator_contingency` / `run_n2_branch_contingency` once the base case solves.
6. `run_dc_opf` → `run_ac_opf` → `run_scopf` for optimization. Pass explicit `lp_solver` / `nlp_solver` only when the deployment requires it.
7. `run_sced` (single-period) and `run_scuc` (multi-period commitment). Call `get_dispatch_request_schema()` before constructing the `request` dict.
8. `compute_nerc_atc` / `compute_ac_atc` for transfer capability. Build source/sink bus lists from `list_buses` output.
9. `export_tables(output_dir)` to hand CSVs back to the user.

## Network construction & editing
For synthetic cases, scenario edits (outage, dispatch change, load scaling), or mutations to a loaded case. Re-solve `run_ac_power_flow` after any material edit.

- **Build:** `create_empty_network`, `add_bus`, `add_generator`, `add_load`, `add_line`, `add_transformer`, `add_storage`.
- **Edit:** `set_branch_rating`, `set_branch_in_service` (outages), `set_generator_limits`, `set_generator_in_service`.
- **Scale:** `scale_loads(factor, area?)`, `scale_generators(factor, area?)`.
- **Remove:** `remove_bus`, `remove_branch`, `remove_generator`, `remove_load`.

## Working rules
- Do not read contingency or sensitivity results from a non-convergent base case.
- Sensitivity tools default to `format="summary"`. Use `"sparse"` or `"full"` only when CSR or dense output is actually needed.
- Solver selection is a deployment question. Default to auto-detect (`"default"`); pass `"highs"` / `"ipopt"` for open-source runs, `"gurobi"` for large MIPs. See `references/SOLVER_GUIDE.md`.
- Call `get_dispatch_request_schema()` before building a `run_sced` / `run_scuc` request dict.
- Hand off RMS / transient-stability questions to ANDES, harmonic / unbalanced questions to OpenDSS.

## Escalation triggers
Map observed violations to the mitigation skill that handles them. If multiple triggers fire, escalate voltage → thermal → contingency.

| Observation | Escalate to |
|---|---|
| Any bus `vm_pu < 0.95` or `> 1.05` | `voltage-violation-mitigation` |
| Any branch loading > 100% of `rate_a_mva` | `thermal-overload-mitigation` |
| `run_n1_*` returns ≥ 1 binding contingency | `contingency-mitigation` |
| `get_islands()` returns > 1 island after a contingency | `contingency-mitigation` |
| SCED / SCUC infeasible, reserve shortage, or LMP volatility | `operations-planning-mitigation` |
| `run_ac_power_flow` fails to converge on the base case | `convergence-failure-mitigation` |
| The study is a new generator, storage, or large-load connection at a POI | `interconnection-impact-mitigation` |

Report the specific numbers that triggered the escalation (bus + vm_pu, branch + loading %, contingency label). Do not say "violations exist" without values.

## Local assets
- `scripts/network_analysis.py` — inspection and base PF review.
- `scripts/sensitivity_analysis.py` — PTDF, LODF drill-down.
- `scripts/contingency_analysis.py` — N-1 / N-2 summaries.
- `scripts/contingency_ranking.py` — N-1 → severity rank → CSV → mitigation-skill mapping. `python contingency_ranking.py <case> <out_dir>`.
- `scripts/opf_analysis.py` — DC / AC / SCOPF with solver-selection examples.
- `scripts/dispatch_analysis.py` — SCED / SCUC.
- `scripts/transfer_capability.py` — NERC ATC and AC ATC path setup.
- `scripts/test_scripts.py` — end-to-end smoke test on a built-in case.
- `references/API_REFERENCE.md` — 44-tool catalog.
- `references/SOLVER_GUIDE.md` — HiGHS / Gurobi / Ipopt selection.
- `references/EXAMPLES.md` — multi-tool workflows.
- `references/DISPATCH_REQUEST_SCHEMA.json` — JSON schema for `run_sced` / `run_scuc` `request`. Also served by `get_dispatch_request_schema()`.

## Report back
- Case loaded (name or path) and key counts from `get_network_info`.
- Base-case convergence. If not converged, stop and report the mismatch.
- Main result of the requested study (violations, LMPs, ATC MW, top sensitivity entries).
- Which mitigation skill is next, if any.
