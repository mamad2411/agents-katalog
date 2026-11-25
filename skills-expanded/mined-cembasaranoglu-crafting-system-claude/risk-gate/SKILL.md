---
name: risk-gate
description: Runs a risk gate for Claude actions. Use when deciding whether to proceed, inspect sources, ask minimum input, plan only, stop, or refuse.
---
# Risk Gate

Assess this task: `$ARGUMENTS`

## Instructions

Score each dimension 0 to 3:

- reversibility
- external impact
- uncertainty
- validation availability
- permission sensitivity

Then choose one decision:

- proceed
- inspect_sources
- ask_minimum_input
- plan_only
- stop
- refuse

Ask only for missing input that is blocking. Do not ask for information already available in source material.

## Output

```yaml
risk_gate_result:
 overall_risk: "low | medium | high | critical"
 score: 0
 decision: "proceed | inspect_sources | ask_minimum_input | plan_only | stop | refuse"
 dimension_scores:
 reversibility: 0
 external_impact: 0
 uncertainty: 0
 validation_availability: 0
 permission_sensitivity: 0
 blockers: []
 non_blocking_assumptions: []
 allowed_actions: []
 forbidden_actions: []
 minimum_user_input_if_blocked: []
```
