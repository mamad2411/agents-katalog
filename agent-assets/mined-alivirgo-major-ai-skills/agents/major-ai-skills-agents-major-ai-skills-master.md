# AGENTS.md

Guidance for coding agents working in this repository.

## Layout

- Canonical skills live at `skills/<id>/SKILL.md`
- Optional model variants: `gpt.md`, `gemini.md` in the same folder
- Registry: `skills_index.json`, `CATALOG.md` (regenerate with `npm run index`)
- Installer: `tools/bin/install.js` (`npx major-ai-skills`)

## Do

- Prefer exact skill IDs over dumping the full catalog into watched agent folders
- Keep skill bodies practical and product-specific
- Run `npm run validate` before opening a PR that touches skills

## Do not

- Commit `.skills-legacy-backup/`
- Invent credentials or destructive one-liners without explicit authorization gates
- Rename a skill folder without updating frontmatter `name:`
