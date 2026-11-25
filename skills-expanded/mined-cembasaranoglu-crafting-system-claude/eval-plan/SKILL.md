---
name: eval-plan
description: Creates an evaluation plan for an agent prompt, skill, or plugin workflow.
  Use when tuning or validating prompt behavior.
---

# Evaluation Plan

Create an eval plan for: `$ARGUMENTS`

## Instructions

1. Define success criteria.
2. Create normal, edge, blocking-gap, high-risk, source-first, adversarial, and regression cases.
3. Define scoring dimensions.
4. Define pass/fail thresholds.
5. Identify what cannot be validated without runtime execution.

## Output

```yaml
eval_plan:
 target_name: ""
 target_type: "prompt | skill | plugin | subagent | mcp_workflow"
 success_criteria: []
 cases:
 - id: "CASE-001"
 category: "happy_path | edge | blocking_gap | high_risk | source_first | adversarial | regression"
 input: ""
 expected_behavior: ""
 scoring: []
 pass_thresholds: {}
 not_validated_here: []
```
