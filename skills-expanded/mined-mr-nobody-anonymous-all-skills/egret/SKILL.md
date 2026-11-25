---
name: egret
description: "Progressive-disclosure workflow for Egret market and operations optimization. Use whenever the user wants to run DC-OPF, AC-OPF, or unit commitment through PowerMCP — even when they just say 'what's the cheapest dispatch', 'commit the units', 'check for congestion', or 'is this schedule feasible'. E"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-tool/skills/egret/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Egret workflow

Start with the cheapest model that can answer the question. Do not jump into unit commitment when a single-snapshot OPF will do.

## Default tool ladder
1. `solve_dc_opf(case_file, solver, return_results)` for fast feasibility and congestion screening.
2. `solve_ac_opf(case_file, solver, return_results)` when voltage or reactive realism matters.
3. `solve_unit_commitment_problem(case_file, solver, mipgap, timelimit)` only after the horizon, reserve logic, and commitment assumptions are clear.

## Working rules
- Confirm the case file format, solver, and time horizon before solving.
- Use DC OPF first unless the question explicitly depends on AC feasibility.
- Treat UC as a higher-cost study that needs a clear operational objective.
- Validate promising dispatch fixes in an AC tool when voltage limits matter.

## Escalation triggers
Quote the binding constraint or infeasibility cause rather than saying "it failed".

| Observation | Escalate to |
|---|---|
| OPF or UC infeasible, reserve-short, or implausibly expensive | `operations-planning-mitigation` |
| AC-OPF bus voltage outside [0.95, 1.05] pu | `voltage-violation-mitigation` |
| A branch limit binds persistently across the horizon | `thermal-overload-mitigation` |

## Deliver
- The case, solver, and study type.
- The limiting constraints or binding tradeoffs.
- Whether the next step is AC validation, UC escalation, or mitigation.
