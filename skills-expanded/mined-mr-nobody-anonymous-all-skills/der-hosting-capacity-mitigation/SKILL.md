---
name: der-hosting-capacity-mitigation
description: "Senior power-engineer playbook for distribution DER integration limits. Use whenever rooftop or utility-scale PV, storage, or other DERs push a feeder into voltage rise, reverse power flow, thermal limits, or protection desensitization — or when the question is how much more DER a feeder can host. T"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-engineering/skills/der-hosting-capacity-mitigation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# DER hosting capacity mitigation

Start by identifying the binding constraint, not by assuming it: hosting capacity is set by whichever of voltage, thermal, or protection binds first on this feeder.

## Preferred action order
1. Confirm the binding constraint with feeder snapshots at minimum load / maximum generation (OpenDSS, pandapower): voltage rise along the feeder, reverse flow at the substation, element loading, and regulator behavior.
2. Use inverter capability first: Volt-VAR and Volt-Watt curves, fixed power-factor settings, or export limits — these are cheap, fast, and usually recover significant headroom.
3. Adjust feeder controls next: regulator and LTC setpoints (including reverse-power mode behavior), capacitor switching coordination with the new flow patterns.
4. Re-check protection: reduced relay reach from DER infeed, sympathetic tripping, fuse-recloser coordination, and anti-islanding behavior under high DER output.
5. Reinforce last: reconductoring, an added regulator, phase rebalancing, or load/DER transfers — and quantify the hosting-capacity gain per upgrade so the cheapest sufficient fix wins.

## Working rules
- Study the minimum-load, maximum-generation snapshot; peak-load studies systematically miss DER constraints.
- Voltage rise and protection usually bind before thermal on weak feeders — do not stop at a loading check.
- Validate any fix across the daily profile (or a time-series run), not a single snapshot; Volt-VAR that fixes noon can misbehave at dusk.
- Legacy regulators may misoperate under reverse flow; check their mode explicitly before relying on them.
- Route persistent voltage problems to `voltage-violation-mitigation` and persistent loading problems to `thermal-overload-mitigation` once the DER-specific levers are exhausted.

## Deliver
- The binding constraint (voltage, thermal, protection) with the numbers and the snapshot that exposed it.
- The mitigation sequence applied, from inverter settings to reinforcement.
- The resulting hosting capacity and the first upgrade that buys the next increment.
