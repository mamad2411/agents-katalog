---
name: adaptive-routing
description: "Classify work and select the cheapest pipeline that preserves expected correctness."
version: 1.0.0
status: active
---
# Adaptive Routing

## Use This Skill When
Use this skill only when the current subtask matches the description. Do not load it globally.

## Procedure
1. OBSERVE scope, ambiguity, blast radius, novelty, and testability.
2. Choose S/M/L/XL using deterministic signals before model judgment.
3. Short-circuit trivial work; add lanes only for independent questions.
4. Escalate only on configured evidence, never prestige.

## Boundaries
- ALWAYS preserve the original task anchor.
- NEVER invent evidence or broaden permissions.
- IF required evidence is missing, THEN return UNKNOWN or block.

## Verify
- Verify selected phases, models, tools, and budgets match the profile.
