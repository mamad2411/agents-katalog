---
name: context-compaction
description: "Compress prior work without losing task constraints or provenance."
version: 1.0.0
status: active
---
# Context Compaction

## Use This Skill When
Use this skill only when the current subtask matches the description. Do not load it globally.

## Procedure
1. Carry the original request verbatim.
2. Preserve exact entities, quantities, paths, IDs, filters, and acceptance criteria.
3. Replace transcripts with evidence cards and artifact hashes.
4. Drop narrative, duplicate facts, and superseded attempts.

## Boundaries
- ALWAYS preserve the original task anchor.
- NEVER invent evidence or broaden permissions.
- IF required evidence is missing, THEN return UNKNOWN or block.

## Verify
- Verify the compact packet can reconstruct the next decision and names every omitted uncertainty.
