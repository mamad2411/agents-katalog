---
name: meaningful-testing
description: "Design tests that prove changed behavior instead of merely executing code."
version: 1.0.0
status: active
---
# Meaningful Testing

## Use This Skill When
Use this skill only when the current subtask matches the description. Do not load it globally.

## Procedure
1. Map tests to acceptance criteria.
2. For bug fixes, add a regression test that fails on the old behavior.
3. Use a negative control or mutation check when feasible.
4. Separate test authorship from execution and verdict.

## Boundaries
- ALWAYS preserve the original task anchor.
- NEVER invent evidence or broaden permissions.
- IF required evidence is missing, THEN return UNKNOWN or block.

## Verify
- Verify the test would fail if the behavioral change were reverted.
