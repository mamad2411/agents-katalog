---
name: documentation
description: "Document only reviewed facts bound to the accepted revision."
version: 1.0.0
status: active
---
# Documentation

## Use This Skill When
Use this skill only when the current subtask matches the description. Do not load it globally.

## Procedure
1. Read the accepted diff and evidence.
2. Update only planned documentation paths.
3. State limitations and operational changes without inventing rationale.
4. Keep proposals separate from observed changes.

## Boundaries
- ALWAYS preserve the original task anchor.
- NEVER invent evidence or broaden permissions.
- IF required evidence is missing, THEN return UNKNOWN or block.

## Verify
- Verify every statement traces to the accepted diff, test evidence, or decision artifact.
