---
name: frontier-escalation
description: "Use a frontier model only for the narrow decision lower tiers cannot resolve."
version: 1.0.0
status: active
---
# Frontier Escalation

## Use This Skill When
Use this skill only when the current subtask matches the description. Do not load it globally.

## Procedure
1. Record the failed lower-tier attempt or qualifying risk trigger.
2. Compress inputs into question, options, evidence, constraints, and decision criterion.
3. Invoke at most once under normal policy.
4. Return the decision downstream to cheap mechanical agents.

## Boundaries
- ALWAYS preserve the original task anchor.
- NEVER invent evidence or broaden permissions.
- IF required evidence is missing, THEN return UNKNOWN or block.

## Verify
- Verify no raw corpus or routine task was sent to the frontier model.
