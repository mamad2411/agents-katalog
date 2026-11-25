---
name: operations-planning-mitigation
description: "Senior power-engineer playbook for planning and operations optimization problems. Use whenever Egret or PyPSA studies are infeasible, reserve-deficient, congested, too expensive, or heavily curtailed — including escalations from a tool skill's OPF, unit-commitment, or expansion run. Triggers on 'OPF"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-engineering/skills/operations-planning-mitigation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Operations and planning mitigation

Start with the failed or unsatisfactory optimization result and the constraint set that caused it.

## Preferred action order
1. Fix data quality first: ramps, minimum output, up or down times, reserve requirements, network limits, and time-series assumptions.
2. Solve a simpler screening case before a larger one: DC before AC, dispatch before unit commitment, operations before expansion.
3. Add flexibility: storage, demand response, fast-start units, or revised reserve products.
4. Relieve congestion with topology, transmission expansion, or better siting.
5. Relax constraints or add slack variables only with explicit penalties and a clear explanation.

## Working rules
- Do not call a system infeasible before checking data consistency.
- Separate economic congestion from physical AC infeasibility.
- Validate promising fixes in an AC tool when voltage or reactive limits matter.

## Deliver
- The main binding constraints or infeasibility cause.
- The best near-term operational fix.
- The longer-term planning measure if the issue persists.
