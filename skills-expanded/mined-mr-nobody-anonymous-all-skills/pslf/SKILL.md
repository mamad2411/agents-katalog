---
name: pslf
description: "Progressive-disclosure workflow for PSLF transmission studies. Use whenever the user wants to open a PSLF case, solve the base power flow, check voltage or overload violations, edit the network (shunts, generators, branches), or run contingency analysis through PowerMCP — even when they just say 'so"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-tool/skills/pslf/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# PSLF workflow

Start with the current case and base power flow. Use network edits and contingencies only after the solved case is credible.

## Default tool ladder
1. `open_case(case)`
2. `solve_case()`
3. `get_voltage(bus)`, `get_voltage_violations(...)`, and `get_overload_violations(...)` to identify the real issue.
4. `add_shunt(...)`, `add_generator(...)`, `add_load(...)`, `add_branch(...)`, or `add_bus(...)` for controlled model changes.
5. `save_case()` after the edited state is worth keeping.
6. `run_contingency_analysis()` only after the base case is solved and monitored.

## Working rules
- Do not run contingencies on an unsolved or obviously bad base case.
- Prefer the smallest corrective action that addresses the violation.

## Escalation triggers
Quote the violated bus or branch and its value rather than saying "violations exist".

| Observation | Escalate to |
|---|---|
| `get_voltage_violations` returns low or high buses | `voltage-violation-mitigation` |
| `get_overload_violations` returns loaded branches | `thermal-overload-mitigation` |
| `run_contingency_analysis` returns binding N-1 cases | `contingency-mitigation` |
| `solve_case` fails to converge | `convergence-failure-mitigation` |

## Deliver
- The case opened and base-case status.
- The key violations found.
- The edits applied and whether the contingency study still fails.
