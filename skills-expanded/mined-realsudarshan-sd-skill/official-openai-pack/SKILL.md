---
name: official-openai-pack
description: Install the Official OpenAI provider pack from Skill Starter Pack.
---

# Official OpenAI Pack

Do not treat this folder as one normal skill. This folder is a bundle manifest for official OpenAI skills collected from GitHub and local Codex cache entries.

When a user installs this pack:

1. Open `paths.txt` in this folder.
2. For each non-empty line, install the skill at:
   `https://github.com/realsudarshan/SD-skill/tree/main/<path-from-paths.txt>`
3. Keep going if one path fails, then report any failed paths clearly.
4. Summarize the installed OpenAI skills.
5. Tell the user: `Restart Codex to pick up the new skills.`

If `paths.txt` is missing or empty, tell the user that this provider pack has no installable skill paths yet.
