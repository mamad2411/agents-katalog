---
name: cursor-pack
description: Explain the Cursor provider pack status in Skill Starter Pack.
---

# Cursor Pack

Do not treat this folder as one normal skill. This folder is a provider-pack manifest.

Cursor currently uses rules and context files rather than installable Codex `SKILL.md` folders in this repository. When a user installs this pack:

1. Open `paths.txt` in this folder.
2. If it contains paths, install each skill at:
   `https://github.com/realsudarshan/SD-skill/tree/main/<path-from-paths.txt>`
3. If it is empty, tell the user no installable Cursor `SKILL.md` paths are currently available.
4. Do not invent Cursor skill paths.
5. Tell the user: `Restart Codex to pick up the new skills.`
