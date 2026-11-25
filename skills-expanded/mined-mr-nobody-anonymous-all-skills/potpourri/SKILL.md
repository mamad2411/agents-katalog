---
name: potpourri
description: "Progressive-disclosure workflow for potpourri (opf-potpourri) AC/DC and multi-period optimal power flow on pandapower distribution networks, including storage and flexible resources. Use whenever the user wants to optimise rather than just simulate a pandapower or SimBench grid — curtail or redispat"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-tool/skills/potpourri/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# potpourri workflow

potpourri builds Pyomo AC/DC OPF models over pandapower networks. There is no
PowerMCP server for it, so drive it through its Python API using the bundled
scripts. Establish a credible network and base case before optimising, and a
credible single period before a multi-period horizon.

## Default ladder
1. `scripts/inspect_case.py --case <simbench:CODE|path.json>` — load, validate,
   and solve the pandapower base case. Do not skip this: an OPF that fails later
   is usually a data problem, and this is where data problems are cheap to find.
2. `scripts/solve_opf.py --list-solvers` — confirm what is installed. AC needs an
   NLP solver (IPOPT); DC needs an LP/MIP solver (GLPK, CBC, HiGHS).
3. `scripts/solve_opf.py --formulation dc --objective ext_grid_import` — linear
   screening for congestion and active-power headroom.
4. `scripts/solve_opf.py --formulation ac --objective <objective>` — the real
   answer whenever voltage, reactive power, losses, or inverter capability matters.
5. `scripts/solve_opf.py --horizon <N> --battery-penetration <pct> --seed <n>` —
   multi-period, only once a single period is credible.

Both scripts print an engineering summary, take `--json` for a machine-readable
payload, and exit non-zero on genuine failure (1 = solved but not optimal,
2 = bad input, 3 = no compatible solver).

## Working rules
- **Never read `net.res_*` without checking termination.** The model constructor
  runs `pp.runpp`, so `net.res_*` is always populated; when a solve is not
  optimal potpourri skips its result mapping and those tables still hold the
  *base case*. `solve_opf.py` reports no results at all in that situation.
- **Multi-period `solve(to_net=True)` writes nothing.** It only logs that it
  did. Map each step with
  `pyo_to_net_multi_period.pyo_sol_to_net_res(net, model, t)`.
- **DC gives no voltage answer.** After a DC OPF `net.res_bus.vm_pu` is a flat
  1.0 placeholder. DC feasibility never establishes AC feasibility, least of all
  in distribution networks where voltage and reactive power are the binding
  physics.
- **A local NLP optimum is not a global one.** IPOPT on a nonconvex AC OPF gives
  a locally optimal point; say "locally optimal", and never claim global
  optimality without a global solver reporting it.
- **Quote numbers, units, and the limit that was configured** — bus and `vm_pu`,
  element and `loading_percent` against its rating, MW/Mvar/MWh, and the solver's
  own termination condition.
- Match the objective to the question and state its side effects: voltage-
  deviation minimisation puts no value on energy, so where curtailment is free it
  will curtail everything. Check the reported curtailment before accepting a
  dispatch.

## Reference material
Read the file that matches what you are doing; do not load them all.
- `references/API_REFERENCE.md` — verified classes, `add_OPF` options, objectives,
  devices, result extraction, and what is *not* supported.
- `references/FORMULATION_GUIDE.md` — AC vs DC, snapshot vs multi-period,
  LP/NLP/MINLP consequences, and single- vs multi-period model differences.
- `references/SOLVER_GUIDE.md` — solver compatibility, termination
  interpretation, and the ordered infeasibility diagnosis.
- `references/VALIDATION_GUIDE.md` — power balance, constraint checks, binding
  constraints, cross-validation against pandapower, and the reporting checklist.

## Local assets in this skill
- `scripts/inspect_case.py` — load, validate, base power flow.
- `scripts/solve_opf.py` — build, solve, validate, and escalate.
- `scripts/test_scripts.py` — smoke tests; skips cleanly without solvers.
- `requirements.txt` — including the `pandapower<3.5` pin potpourri needs.

## Escalation triggers
Quote the element, value, unit, and configured limit that tripped each row.
`solve_opf.py` emits these in its `escalation` payload.

| Observation | Escalate to |
|---|---|
| Bus `vm_pu` outside the configured `[min_vm_pu, max_vm_pu]` band (AC only) | `voltage-violation-mitigation` |
| `res_line` / `res_trafo` `loading_percent` above its configured `max_loading_percent` | `thermal-overload-mitigation` |
| `termination_condition` is `infeasible` or `unbounded`, or curtailment exceeds 5 % of available renewable energy | `operations-planning-mitigation` |
| Solve ends in any other non-optimal condition (`other`, `maxIterations`, `maxTimeLimit`), or the base `pp.runpp` fails | `convergence-failure-mitigation` |
| Net export through the external grid, or PV-driven voltage rise on a distribution feeder | `der-hosting-capacity-mitigation` |
| A newly added generator, storage unit, or large load causes any of the above | `interconnection-impact-mitigation` |

## Deliver
- Network source and size, study type and formulation, horizon and resolution.
- Objective, what it means in units, and the solver plus its termination condition.
- Power balance, voltage extrema with buses, worst line and transformer loading,
  dispatch by group, curtailment, and storage SOC extrema where relevant.
- Binding constraints, and limitations (local optimum, DC assumptions, storage
  modelling caveats).
- Any justified escalation, with the numbers behind it.
