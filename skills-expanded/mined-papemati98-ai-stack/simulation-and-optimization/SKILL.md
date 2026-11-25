---
name: simulation-and-optimization
description: Design and evaluate simulations and optimizers with explicit units, uncertainty, V&V, Pareto tradeoffs and fail-closed control gates. Includes an energy-specific ladder; no automatic control or deployment.
---

# Simulation and Optimization

Use this skill for a bounded model, scenario study, optimizer or policy benchmark.
Start with the simplest defensible model and keep simulation, optimization and
execution as separate trust boundaries.

## Workflow

1. Define use case, state/actions, objective, constraints, units, time base and
   uncertainty. Record source, calibration data and assumptions.
2. Establish a rule or analytical baseline, then verify implementation against
   invariants and known cases.
3. Validate scenarios and sensitivity; report V&V evidence, uncertainty and
   failure modes before tuning an optimizer.
4. Compare feasible solutions on objective, constraint violations, robustness,
   cost and latency. For multiple objectives, report the Pareto set and tradeoffs.
5. For energy systems follow the ladder in the reference: heuristic, MILP/MPC,
   forecast plus optimizer, evolutionary search, RL last.
6. A control candidate remains shadow-mode only until safety envelope, fallback,
   OOS validation, human approval and independent acceptance are complete.

Read [references/contract.md](references/contract.md) and
[references/trigger-cases.json](references/trigger-cases.json).

**Optional, only when a mechanism illustration of a model or policy is requested**: read
[references/mechanism-explainers.md](references/mechanism-explainers.md) for bounded
explainer patterns (single state model, geometry invariants, contact-sheet checkpoints,
accessible alternatives, visible simplifications). Normal sessions add no reference reads,
model calls, or work steps; this link adds a small static prompt-token cost. Simulation,
optimization and execution stay separate trust boundaries and no live control is implied.
