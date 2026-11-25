---
name: thermal-overload-mitigation
description: "Senior power-engineer playbook for overloaded lines and transformers. Use whenever power-flow or contingency studies show loading above ratings — including escalations from a tool skill where branch loading exceeds 100% of its rating. Triggers on 'line overloaded', 'transformer above rating', 'relie"
category: electrical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Power-Agent/PowerSkills"
source_repository: "Power-Agent/PowerSkills"
source_path: "powerskills-engineering/skills/thermal-overload-mitigation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Thermal overload mitigation

Start with the monitored element, the applicable rating, and the driving condition.

## Preferred action order
1. Confirm the overload is real: correct rating set, correct outage state, and solved base case or contingency.
2. Redispatch generation or transfer patterns to unload the corridor.
3. Reconfigure topology or switching where operations permit.
4. Use phase shifters, HVDC schedules, or transformer controls only when sensitivity evidence supports them.
5. If the issue is persistent, move to reconductoring, uprating, or new facilities.
6. After each action, re-solve and confirm the overload is relieved. If it is not, continue to the next step.

### Worked example
Line A-B sits at 105% of its normal rating after the N-1 loss of Line C-D. The PTDF for a
G3-to-G5 transfer on Line A-B is -0.18 MW/MW, so shifting 40 MW off G3 onto G5 unloads
A-B by about 7 MW, bringing it to 94%. Re-solving the full monitored contingency set
confirms the redispatch creates no new violations elsewhere.

## Working rules
- Separate normal-rating issues from emergency-rating issues.
- Fix the smallest set of elements that relieve the monitored overload cluster.
- Validate a candidate fix on all critical monitored contingencies, not just the worst case.
- Use PTDF or LODF style sensitivities when the software provides them.

## Deliver
- The overloaded elements and rating basis.
- The dispatch or topology changes that help most.
- The recommended corrective action and the residual risk.
