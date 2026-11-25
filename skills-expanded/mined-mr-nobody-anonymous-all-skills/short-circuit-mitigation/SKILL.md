---
name: short-circuit-mitigation
description: "Senior power-engineer playbook for excessive fault current and breaker over-duty. Use whenever a short-circuit study shows fault duty above interrupting ratings, or a new interconnection raises fault levels near equipment limits. Triggers on 'fault duty', 'breaker over-duty', 'short-circuit current"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-engineering/skills/short-circuit-mitigation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Short-circuit mitigation

Start with the over-dutied buses and breakers, the fault type, and the study assumptions that produced them.

## Preferred action order
1. Confirm the duty is real: machine subtransient data, motor contribution, pre-fault voltage assumption, fault type (three-phase vs single-line-to-ground), and the X/R used for asymmetry — over-duty findings are often data findings.
2. Apply operational fixes first: split buses, open bus-tie or loop points, and re-dispatch nearby generation where switching alone relieves the duty.
3. Add impedance on the offending paths: series reactors or higher-impedance transformer choices for new connections.
4. Screen fault-current limiters where switching and impedance are not enough.
5. Recommend breaker replacement or uprating as the planning fix, with an interim operating guide until installed.

## Working rules
- Check maximum (all-sources-in) and minimum (credible outage) fault cases — protection settings need the minimum, breaker duty needs the maximum.
- Single-line-to-ground duty can exceed three-phase duty near grounded transformer banks; do not screen on three-phase faults alone.
- Bus splitting changes power-flow transfer paths and N-1 performance; re-run the contingency screen after any topology fix and route findings to `contingency-mitigation`.
- Keep the protection engineer in the loop: any fix that changes fault levels changes relay reach.

## Deliver
- The over-dutied equipment, its rating basis, and the computed duty.
- The mitigation sequence tried, from switching to reinforcement.
- The residual duty margin and any protection re-coordination still required.
