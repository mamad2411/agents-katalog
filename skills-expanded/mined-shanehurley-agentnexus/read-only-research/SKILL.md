---
name: read-only-research
description: "Gather narrow evidence without mutating the target."
version: 1.0.0
status: active
---
# Read Only Research

## Use This Skill When
Use this skill only when the current subtask matches the description. Do not load it globally.

## Procedure
1. Assign one question per lane.
2. Read primary sources first and cite exact paths or URLs.
3. Return bounded evidence cards; omit recommendations.
4. Mark contradictions and UNKNOWN values explicitly.

## Boundaries
- ALWAYS preserve the original task anchor.
- NEVER invent evidence or broaden permissions.
- IF required evidence is missing, THEN return UNKNOWN or block.

## Verify
- Verify no write-capable tool was called and every finding has provenance.
