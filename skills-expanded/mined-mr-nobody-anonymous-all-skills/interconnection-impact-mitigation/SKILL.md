---
name: interconnection-impact-mitigation
description: "Senior power-engineer playbook for screening and mitigating the grid impact of a new generator, storage, or large-load interconnection. Use whenever the question is whether X MW can connect at a point of interconnection and what upgrades it needs. Triggers on 'interconnection study', 'system impact"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-engineering/skills/interconnection-impact-mitigation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Interconnection impact mitigation

Start with a defined injection: MW and MVAr capability, the point of interconnection (POI), and the dispatch scenarios to study.

## Preferred action order
1. Pin down the study scenario set: peak and off-peak cases, high-renewable dispatch, and the prior-queued projects that must be modeled as in-service.
2. Run steady-state screens with the addition: base case and N-1 power flow, thermal loading and voltage screens around the POI. Route violations to `thermal-overload-mitigation` and `voltage-violation-mitigation` for the corrective toolkit.
3. Check weak-grid risk for inverter-based resources: short-circuit ratio at the POI. Low SCR (roughly below 3, critical below 2) flags control-interaction and stability risk — consider grid-forming controls, synchronous condensers, or POI relocation.
4. Verify reactive capability and voltage control: power-factor range and voltage ride-through at the POI against the applicable interconnection requirements.
5. Identify the binding constraint and assemble the mitigation set: network upgrades, an output-limitation or curtailment agreement, reactive devices, or phased interconnection — sized to the smallest set that clears the binding screen.

## Working rules
- Screen with linear tools (PTDF on the injection) before full N-1 reruns; confirm the short list in AC.
- The fault contribution of the new plant changes breaker duty nearby; screen it and route over-duty to `short-circuit-mitigation`.
- Restudy after any material change in plant size, POI, or queue assumptions — interconnection results do not transfer between scenarios.
- Separate "needed to connect safely" from "needed to deliver full output" — reliability upgrades and deliverability upgrades have different urgency and cost allocation.

## Deliver
- The injection studied (MW, POI, scenarios) and the screens it passed.
- The binding constraint with numbers (element, loading or voltage, contingency).
- The recommended mitigation set and what must be restudied if assumptions move.
