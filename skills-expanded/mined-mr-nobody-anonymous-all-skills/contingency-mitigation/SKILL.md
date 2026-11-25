---
name: contingency-mitigation
description: "Senior power-engineer playbook for contingency violations. Use whenever N-1 or N-2 studies reveal voltage or thermal problems, binding contingencies, or post-outage islanding — including escalations from a tool skill's contingency run. Triggers on 'N-1 violation', 'worst contingency', 'preventive vs"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-engineering/skills/contingency-mitigation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Contingency mitigation

Start with a solved base case and a ranked list of critical contingencies.

## Preferred action order
1. Verify the contingency definitions, monitored elements, and limits.
2. Group critical contingencies by common corridor, interface, or weak area.
3. Apply preventive actions first: redispatch, shunts, tap changes, or topology changes that help multiple contingencies.
4. Evaluate corrective actions next: post-contingency switching, redispatch, or RAS schemes with explicit triggers.
5. Re-run the full monitored set after any candidate fix. If violations remain, return to step 3 with updated rankings.
6. Use load shedding only as a last-resort action and state that clearly.
7. For recurring problems, recommend reinforcement or a revised operating guide.

### Worked example
The N-1 loss of Line X-Y overloads Line A-B to 108% of rating and pulls Bus C down to
0.91 pu. Grouping the violations shows both sit on the same east-west corridor, so one
preventive action can cover the family: 60 MW of redispatch from G1 to G4 clears the
thermal violation, and switching in the 50 Mvar capacitor bank at Bus C restores the
voltage to 0.97 pu. Re-running every monitored contingency confirms no new violations.

## Working rules
- Do not trust contingency results from a bad base case.
- Prefer actions that improve a family of contingencies rather than a single outage.

## Deliver
- The critical contingencies and the shared weak pattern.
- The best preventive action.
- Any corrective action that is still required after prevention.
