---
name: skill-starter-pack
description: Guided router for Skill Starter Pack install commands and bundles.
---

# Skill Starter Pack

Do not immediately install everything just because the user pointed you at this repository.

This repo is an install guide and bundle index for AI-agent skills. Treat it as a router:

1. Ask what the user is setting up.
2. Offer focused choices: favourites, my originals, reccomended, a scenario category, a provider pack, specific skills, or everything.
3. If the user knows the kind of work they do, recommend matching folders from `categories/`.
4. Open the matching folder's `SKILL.md` and follow its `paths.txt` install instructions.
5. If the user says they want everything, use `categories/full-startup/SKILL.md`.
6. After installing, tell the user: `Restart Codex to pick up the new skills.`

Useful entry points:

- `favourites/SKILL.md`
- `originals/SKILL.md`
- `reccomended/SKILL.md`
- `categories/SKILL.md`
- `categories/full-startup/SKILL.md`
- `categories/web-development-setup/SKILL.md`
