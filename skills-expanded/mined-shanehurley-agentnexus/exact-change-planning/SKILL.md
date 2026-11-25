---
name: exact-change-planning
description: "Convert a frozen decision into mechanical, reversible change units."
version: 1.0.0
status: active
---
# Exact Change Planning

## Use This Skill When
Use this skill only when the current subtask matches the description. Do not load it globally.

## Procedure
1. Name exact paths and symbols or regions.
2. State behavior before and after.
3. Map each acceptance criterion to a test and verification command.
4. Declare file allowlists, rollback, dependencies, and ordering.
5. Reject the plan if any implementer decision remains.

## Boundaries
- ALWAYS preserve the original task anchor.
- NEVER invent evidence or broaden permissions.
- IF required evidence is missing, THEN return UNKNOWN or block.

## Verify
- Verify unresolved_questions is empty and every write is allowlisted.
