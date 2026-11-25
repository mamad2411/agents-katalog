---
name: skillpack-harvest
description: Lift a proven skill from another repo into this skillpack with privacy review and validation.
---

# Skillpack Harvest

Use this skill when the user wants to bring a useful workflow from another repo into this port.

## Workflow

1. Identify the source skill and license/privacy constraints.
2. Read the workflow and remove repo-private details.
3. Adapt it to Codex and this repo's registry shape.
4. Add or update routing only if the trigger is broadly useful.
5. If a native plugin manifest is present, update its skill registry without
   removing unrelated install-required fields, configuration schemas, or
   contracts.
6. Validate the repo and summarize provenance.

## Guardrails

- Do not import secrets, private URLs, or user-specific data.
- Do not copy licensed material without permission.
- Keep the harvested skill maintainable and short.
