---
name: industrial-systems
description: |
  Industrial and physical systems: power/energy optimization, HVAC/PID control,
  routing/scheduling, process constraints, and simulation-in-the-loop tuning.
  Use for OPF/unit-commitment-style tasks, control setpoints, BGP/network
  operations with physical/logical constraints, and manufacturing scheduling
  — not for pure software debugging or math tasks with no physical
  constraint set.
---

# industrial-systems

Load `safe-agent-scope` before any state-changing action; industrial/control tasks do not waive sandbox, recipient, or injection rules.

## Why

These tasks encode **hard constraints** (capacity, stability, safety limits).
A high objective value that violates constraints is a fail. Model the
feasible set before optimizing.

## Procedure

1. **List constraints** — equalities/inequalities, bounds, ramping, exclusivity.
2. **Choose representation** — LP/MIP/CP/heuristics based on what's available
   (OR-Tools, pandapower-like, custom sim).
3. **Baseline** — feasible naïve solution before optimizing.
4. **Optimize** — clear objective; log solver status (optimal/feasible/infeasible).
5. **Validate** — re-check every constraint on the exported schedule/setpoints.
6. **Export** — exact schema; `verify-task-output`.

## Heuristics

- Infeasible? relax only what the instruction allows — report conflict otherwise
- Prefer interpretable setpoints over black-box controllers when grading is analytic
- Time-indexed decisions: align timesteps with the simulator's dt

## Anti-patterns

- Ignoring thermal/voltage/capacity limits to chase objective
- Unit mismatches (MW vs kW, °C vs K)
- Returning solver-best without a constraint audit
