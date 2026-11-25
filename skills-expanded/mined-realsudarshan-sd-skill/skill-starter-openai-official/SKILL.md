---
name: skill-starter-openai-official
description: Install the Skill Starter Pack official OpenAI provider bundle by following this folder's paths.txt.
---

# Official OpenAI Bundle

Use this when the user asks for official OpenAI skills or OpenAI provider setup.

Do not treat this folder as one normal skill. This folder is a bundle manifest.

1. Open `paths.txt` in this folder.
2. For each non-empty line, install the skill at `https://github.com/realsudarshan/SD-skill/tree/main/<path>`.
3. Show the user the skills you installed.
4. If any path fails, report that exact path and continue with the remaining paths.
5. After installing, tell the user: `Restart Codex to pick up the new skills.`
