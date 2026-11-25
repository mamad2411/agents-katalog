---
name: stale-global-skill-assumption-invalid
description: Invalid stale global skill assumption fixture.
version: v0.0
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell. Global skills are always valid.
