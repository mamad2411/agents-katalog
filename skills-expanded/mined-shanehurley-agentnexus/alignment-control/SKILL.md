---
name: alignment-control
description: "Prevent technically valid work from drifting away from user intent."
version: 1.0.0
status: active
---
# Alignment Control

## Use This Skill When
Use this skill only when the current subtask matches the description. Do not load it globally.

## Procedure
1. Compare request→decision→plan→diff→tests→docs.
2. Treat all/only/each, quantities, names, and exclusions as invariants.
3. Reject extra scope even when beneficial.
4. Route mismatch to the earliest responsible phase.

## Boundaries
- ALWAYS preserve the original task anchor.
- NEVER invent evidence or broaden permissions.
- IF required evidence is missing, THEN return UNKNOWN or block.

## Verify
- Verify every requested outcome is covered and no unrequested outcome was introduced.
