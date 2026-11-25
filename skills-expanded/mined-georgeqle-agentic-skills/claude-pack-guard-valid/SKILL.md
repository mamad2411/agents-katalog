---
name: claude-pack-guard-valid
description: Valid Claude Pack Availability Guard fixture.
version: v0.0
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `npx skillpacks install <pack>` from the project shell. After install, tell Claude users to run `/reload-skills`, then `/clear` or restart if the skill remains invisible.
