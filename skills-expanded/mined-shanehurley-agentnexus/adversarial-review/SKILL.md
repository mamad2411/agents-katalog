---
name: adversarial-review
description: "Try to disprove a plan or change using primary evidence."
version: 1.0.0
status: active
---
# Adversarial Review

## Use This Skill When
Use this skill only when the current subtask matches the description. Do not load it globally.

## Procedure
1. Inspect the plan or diff before author commentary.
2. Prioritize correctness, scope, security, compatibility, and missing tests.
3. Provide evidence and a concrete mitigation for every blocking finding.
4. Approve only after naming checks performed.

## Boundaries
- ALWAYS preserve the original task anchor.
- NEVER invent evidence or broaden permissions.
- IF required evidence is missing, THEN return UNKNOWN or block.

## Verify
- Verify the reviewer is distinct from the author and remained read-only.
