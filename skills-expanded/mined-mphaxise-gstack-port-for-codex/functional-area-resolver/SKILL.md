---
name: functional-area-resolver
description: Compress large routing files into functional-area dispatch rules while preserving discoverability.
---

# Functional Area Resolver

Use this skill when a routing file, resolver, or agent instruction set has become too granular to scan.

## Workflow

1. Read the current routing file.
2. Group skills or actions by functional area.
3. Replace repetitive rows with dispatcher entries that list included sub-skills.
4. Preserve special-case triggers that change behavior materially.
5. Validate that important skills remain discoverable.

## Guardrails

- Do not remove safety or permission rules.
- Do not hide rare but dangerous workflows in vague categories.
- Keep the resulting resolver easier to use than the original.
