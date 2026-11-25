---
name: voltage-violation-mitigation
description: "Senior power-engineer playbook for voltage violations. Use whenever a base-case or contingency study shows low voltage, high voltage, weak reactive support, or tap exhaustion — including escalations from a tool skill where bus voltage falls below 0.95 pu or rises above 1.05 pu in PowerWorld, PSS/E,"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-engineering/skills/voltage-violation-mitigation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Voltage violation mitigation

Start only after the violated buses, limits, and study condition are known.

## Preferred action order
1. Confirm the violation is real: solved case, correct limits, realistic generator Q limits, working AVR or Volt-VAR controls, correct remote-regulation targets.
2. Use existing reactive support first: generator voltage setpoints, free LTCs, switch shunts or capacitors, enable SVC or STATCOM or inverter Volt-VAR response.
3. Reduce reactive transport: redispatch MW closer to load, reduce stressed imports, or reconfigure topology.
4. If the problem remains, reduce transfer or load and identify reinforcement needs.

## High-voltage cases
- Lower voltage targets carefully.
- Switch out capacitors or switch in reactors.
- Absorb vars with generators or inverters where capability exists.
- Re-check light-load and outage conditions separately.

## Software cues
- PowerWorld, PSLF, and PSSE: adjust shunts, taps, and generator controls, then re-solve.
- OpenDSS: regulators, capacitor banks, and inverter controls come before feeder rebuilds.
- pandapower: shunts, tap settings, and generator Q support are the first levers.
- PyPSA or Egret: use them to screen dispatch or transfer fixes, then validate voltage with an AC tool.

## Deliver
- The violated buses and condition.
- The mitigation sequence tried or recommended.
- The first action that clears the issue without creating a worse one.
