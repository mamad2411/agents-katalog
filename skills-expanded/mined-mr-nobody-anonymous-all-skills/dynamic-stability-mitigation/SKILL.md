---
name: dynamic-stability-mitigation
description: "Senior power-engineer playbook for dynamic stability problems. Use whenever eigenvalue or time-domain studies show poor damping, transient angle instability, weak voltage recovery, or sustained oscillations in tools such as ANDES or PSS/E — including escalations from a tool skill's dynamic run. Trig"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-engineering/skills/dynamic-stability-mitigation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Dynamic stability mitigation

Start only after the disturbance, monitored channels, and failing metric are explicit.

## Preferred action order
1. Confirm the models and event setup are credible: machine data, control models, fault location, clearing time, and initial dispatch.
2. Reduce the stressed transfer or dispatch pattern that drives the instability.
3. Improve controls: AVR, PSS, governor, FACTS, or dynamic VAR support.
4. Improve protection or switching performance if clearing time is the binding issue.
5. Consider RAS, fast valving, braking resistors, or controlled load shedding only with explicit trigger logic.

## Working rules
- Use eigenvalues to screen and time-domain simulation to confirm.
- Separate angle instability, oscillatory instability, and voltage recovery problems; they do not share the same fix order.
- Re-check the steady-state dispatch after major control or topology changes.

## Deliver
- The failing mode or scenario.
- The mitigation sequence that should be tried.
- The first credible fix and the remaining validation needed.
