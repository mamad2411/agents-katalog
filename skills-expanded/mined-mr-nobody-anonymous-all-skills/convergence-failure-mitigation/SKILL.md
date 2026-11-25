---
name: convergence-failure-mitigation
description: "Senior power-engineer playbook for power-flow convergence failures. Use whenever a base case or post-change case diverges, oscillates, or fails to solve in PSS/E, PSLF, PowerWorld, pandapower, PyPSA, surge, or OpenDSS. Triggers on 'power flow diverged', 'case won't solve', 'did not converge', 'blown"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-engineering/skills/convergence-failure-mitigation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Convergence failure mitigation

Start from the failed solve and its mismatch report. The goal is to learn *why* it failed, not just to force a solution.

## Preferred action order
1. Rule out data problems first: isolated or de-energized buses, zero or absurd branch impedances, missing or misplaced swing bus, transformer tap and phase-angle data, load/generation totals that cannot balance.
2. Check islanding and slack coverage: every energized island needs a slack with feasible MW. Use the tool's island or topology report before touching solver settings.
3. Simplify the solve, then restore: try flat start vs warm start, lock taps, switched shunts, and phase shifters, relax generator Q-limits — then re-enable controls stepwise once a solution exists.
4. Seed from an easier point: a DC solve, a previously solved neighbor case, or a reduced-stress version of the case, then scale load or transfer toward the target in steps.
5. If failure persists only near the target stress level, treat it as a feasibility boundary, not a numerical bug: reduce transfer or load, add reactive support, and flag possible voltage-collapse proximity.

## Working rules
- The largest mismatch bus tells you where to look — start there, not with global solver settings.
- Change one solver setting at a time and record what finally solved.
- A case solved with controls locked or Q-limits relaxed is not finished; restore realism before reporting results from it.
- Distinguish "the math failed" from "the operating point does not exist" — the corrective actions are completely different.

## Deliver
- The failure category: data error, control interaction, numerical fragility, or physical infeasibility.
- The specific change that made the case solve.
- Any realism caveats that remain (locked controls, relaxed limits) and what to re-check.
