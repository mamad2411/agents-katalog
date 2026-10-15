---
name: skilly-cli
description: Manage this repo's agent skills with the skilly CLI — add or remove bundles/skills, pull hub updates. Use when the user wants skills or bundles added, removed, or updated. For a skills.sh URL use the skills CLI directly, not skilly. Not for repo bootstrap (that is `skilly setup`, run once).
---

# Skilly CLI

This repo's skills are managed by skilly, a hub at `timschoch/skilly`. Always use the CLI; never install skills by manual copies.

Exception — the user posts a skills.sh URL: that skill lives outside the hub. Hand-pin it with the skills CLI: `npx -y skills add <url> --agent claude-code -y`. It lands in `skills-lock.json` and survives the sync; skilly never touches hand-pins.

- Add a bundle or single skill: `npx -y github:timschoch/skilly add <name...>` — bundle names and what they contain: [catalog](https://github.com/timschoch/skilly/blob/main/docs/bundles.md)
- Remove: `npx -y github:timschoch/skilly remove <name...>` — removing a bundle keeps skills still claimed by another bundle
- Pull the hub's current state: `npx -y github:timschoch/skilly update`

Every verb ends with its own commit, push, and PR — do not commit or push for it. On `main` it branches to `chore/skilly-setup` by itself.

Never hand-edit skilly-owned files — the nightly sync wipes and rewrites them:

- `.claude/skills/` and `.agents/skills/` (installed skills)
- `.claude/rules/<name>-*.md` (installed router rules)
- `.skilly.json`, `skills-lock.json`

A change to a skill belongs in its source repo (see `skills-lock.json` for the source), a repo-local rule in `CLAUDE.md`.
