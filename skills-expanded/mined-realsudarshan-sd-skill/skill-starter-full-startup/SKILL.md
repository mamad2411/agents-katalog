---
name: skill-starter-full-startup
description: Install the full Skill Starter Pack catalog by following this folder's paths.txt.
---

# Full Startup Bundle

Use this only when the user explicitly wants the full catalog.

Do not treat this folder as one normal skill. This folder is a bundle manifest.

1. Open `paths.txt` in this folder.
2. For each non-empty line, install the skill at `https://github.com/realsudarshan/SD-skill/tree/main/<path>`.
3. Show the user the skills you installed.
4. If any path fails, report that exact path and continue with the remaining paths.
5. After installing, tell the user: `Restart Codex to pick up the new skills.`
