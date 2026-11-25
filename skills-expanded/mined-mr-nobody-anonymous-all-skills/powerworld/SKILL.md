---
name: powerworld
description: "Progressive-disclosure workflow for PowerWorld Simulator studies through PowerMCP. Use whenever the user wants to open a PowerWorld case, solve the base power flow, inspect flows or voltages, change model data, run contingency analysis, or pull sensitivity matrices (PTDF, LODF, Jacobian, Ybus) — eve"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-tool/skills/powerworld/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# PowerWorld workflow

Expose PowerWorld tools in stages. Start with the base case. Move to contingencies or matrix analytics only after the operating condition is understood.

## Default tool ladder
1. `open_case(case_path)`
2. `run_powerflow(solution_method)`
3. `get_power_flow_results(object_type, additional_fields)` and `get_key_field_list(object_type)`
4. `change_and_confirm_params(...)` or `change_parameters_multiple_element(...)`
5. `analyze_contingencies(option, validate)`
6. `get_ybus()`, `get_jacobian()`, `get_lodf_matrix()`, `get_ptdf_matrix_fast()`, `to_graph()`, `determine_shortest_path()`, or `run_robustness_analysis()`

## Working rules
- Do not run contingencies before the base case solves cleanly.
- Ask for the monitored objects, limits, and fields before large result pulls.
- Use sensitivities or graph tools to rank candidate fixes before applying bulk changes.
- Confirm every model change by re-solving and checking the same monitored quantities.

## Escalation triggers
Quote the bus or branch and the value that tripped each row rather than saying "violations exist".

| Observation | Escalate to |
|---|---|
| Bus voltage outside [0.95, 1.05] pu in the power-flow results | `voltage-violation-mitigation` |
| Branch percent loading > 100 | `thermal-overload-mitigation` |
| `analyze_contingencies` returns binding violations | `contingency-mitigation` |
| `run_powerflow` fails to converge | `convergence-failure-mitigation` |

## Deliver
- The case, base-case status, and monitored findings.
- Any changes applied and their effect.
- Whether an advanced study or mitigation playbook is required next.
