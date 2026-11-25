---
name: pypsa
description: "Progressive-disclosure workflow for PyPSA studies. Use whenever the user wants to load or build a PyPSA network, inspect components or time series, run power flow, solve operational OPF, or run capacity-expansion / investment optimization — even when they just say 'optimize the dispatch', 'size the"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-tool/skills/pypsa/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# PyPSA workflow

Start by creating or loading a named network handle. Use network inspection before optimization, and use operational optimization before investment optimization.

## Default tool ladder
1. `load_network(file_path)` or `create_network(...)` to create the active network handle.
2. `get_network_info(network_name)` and `get_component_details(...)` to understand topology, assets, and time series.
3. `run_power_flow(network_name, linear=False)` for feasibility checks.
4. `optimize_network(network_name, ...)` for dispatch or operational studies.
5. `optimize_investment(network_name, ...)` for expansion questions.
6. `import_from_csv_folder(...)` or `export_to_csv_folder(...)` once the network state is worth moving.

### Example sequence
Using the `case39.nc` network shipped with this skill:
```
load_network("case39.nc")                        -> network "case39" active, 39 buses
get_network_info("case39")                       -> 10 generators, 46 branches, 19 loads
run_power_flow("case39", linear=False)           -> converged, max branch loading 87%
optimize_network("case39", solver_name="highs")  -> feasible dispatch, hourly cost reported
```
Feasibility first, then dispatch. Only move to `optimize_investment` once a dispatch
study cannot answer the question.

## Working rules
- Do not jump straight into expansion optimization when a dispatch study can answer the question.
- Use AC or DC power flow to sanity-check a network before relying on optimization outputs.
- Treat PyPSA as a planning and scheduling engine, not the final authority on detailed reactive mitigation.

## Escalation triggers
Quote the numbers that tripped each row (bus + v_mag_pu, element + loading, infeasibility cause) rather than saying "it failed".

| Observation | Escalate to |
|---|---|
| Bus `v_mag_pu` < 0.95 or > 1.05 on an AC power flow | `voltage-violation-mitigation` |
| Line or transformer loaded > 100% of `s_nom` | `thermal-overload-mitigation` |
| `run_contingency_analysis` N-1 overload or post-outage islanding | `contingency-mitigation` |
| `optimize_network` / `optimize_investment` infeasible, reserve-short, or heavily curtailed | `operations-planning-mitigation` |
| `run_power_flow` fails to converge | `convergence-failure-mitigation` |

## Local assets in this skill
- `case39.nc` — a ready test network.
- `scripts/network_analysis.py` — inspection.
- `scripts/optimization_analysis.py` — OPF result review.
- `scripts/expansion_analysis.py` — capacity-expansion studies.
- `scripts/contingency_analysis.py` — local N-1 screening outside PowerMCP.

## Deliver
- The network handle and study type.
- The main feasibility or cost result.
- Whether the next step is mitigation, AC validation, or a larger optimization.
