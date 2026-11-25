---
name: frequency-response-mitigation
description: "Senior power-engineer playbook for frequency-performance problems. Use whenever studies or operations show low system inertia, poor frequency nadir, high RoCoF, weak primary frequency response, UFLS encroachment, or reserve shortfall after loss of the largest unit or HVDC import. Triggers on 'freque"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-engineering/skills/frequency-response-mitigation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Frequency response mitigation

Start only after the design event and the failing metric are explicit: which contingency, and which of nadir, RoCoF, or settling frequency violates its limit.

## Preferred action order
1. Confirm the study setup is credible: largest credible loss, load-damping assumption, governor models actually enabled and responsive (deadbands, baseload flags), and the inertia of the dispatch being studied.
2. Increase responsive headroom first: commit or back down units to create governor headroom, and enable fast frequency response from storage, IBRs, or demand response — MW that respond in the first seconds matter most.
3. Raise inertia where headroom alone is insufficient: additional synchronous units, synchronous condensers (with flywheels where available), and must-run rules for low-inertia hours.
4. Fix control settings: droop, deadband, and response-withdrawal behavior so primary response is sustained, not transient.
5. Re-coordinate UFLS last — it is the backstop that protects the system when the fixes above fall short, not the fix itself.

## Working rules
- Evaluate the worst inertia hour (high renewables, light load), not the average dispatch.
- Screen with system-level metrics, then confirm the critical cases in time domain (ANDES, PSS/E) before claiming the fix works.
- Track the response *trajectory*: a good nadir with rapid response withdrawal can still fail the settling-frequency requirement.
- Frequency containment and oscillation damping are different problems; route poorly damped responses to `dynamic-stability-mitigation`.

## Deliver
- The design event and the violated metric (nadir, RoCoF, settling frequency) with values.
- The mitigation sequence: headroom, fast response, inertia, control fixes.
- The first credible fix and the time-domain validation still needed.
