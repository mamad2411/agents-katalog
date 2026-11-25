---
name: codex-base-skill-fallback-valid
description: Valid Codex base skill fallback fixture.
version: v0.0
---

### Missing Skill Fallback

If not found in any pack, suggest `$skills` or `$skills search <keyword>` only when `$skills` is visible in the active session; otherwise recommend `npx skillpacks init` from the project shell to install base skills, or use `npx skillpacks which <skill-name>` for a direct package lookup.
