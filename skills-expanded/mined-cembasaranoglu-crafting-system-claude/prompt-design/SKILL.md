---
name: prompt-design
description: Designs a new Claude prompt system with operating contract, modes, risk gate, tool policy, output schemas, examples, and eval plan. Use when creating a reusable prompt.
---
# Prompt Design

Design a Claude prompt system for: `$ARGUMENTS`

## Instructions

1. Ask for missing input only if it is blocking and cannot be inferred safely.
2. Define target surface and operating mode.
3. Create a prompt architecture with:
 - operating identity
 - priority order
 - source precedence
 - truth rules
 - readiness gate
 - risk gate
 - tool policy
 - workflow
 - output schemas
 - examples
 - evaluation plan
4. Keep the prompt modular and versionable.
5. Mark assumptions explicitly.

## Output

```yaml
prompt_design:
 status: "ready | partially_ready | blocked"
 prompt_name: ""
 target_surface: ""
 assumptions: []
 blockers: []
 artifacts:
 - prompt_operating_contract
 - risk_gate
 - tool_policy
 - output_schema
 - eval_plan
```

Then provide the draft prompt in markdown.
