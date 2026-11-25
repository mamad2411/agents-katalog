---
name: ai-context
description: >
  Updating AGENTS.md, CLAUDE.md, adding new skills, or maintaining the agent context
  system in this repo. Use when adding a new skill, updating the skills index, or
  when an agent keeps getting something wrong and the docs need refinement.
---

# AI Context Maintenance

How to keep this repo's agent documentation accurate and useful.

## Adding a New Skill

1. Create `.github/skills/<topic>/SKILL.md` with YAML frontmatter (name + description)
2. Add a row to the skills table in **both** `AGENTS.md` and `CLAUDE.md`
3. Keep the description "pushy" — describe triggers broadly so agents actually load it

## Adding a New Template

1. Create `templates/<source>/<template-name>/`
2. Drop the exported zip contents there
3. Add a `README.md` inside noting: what it is, what's inspiring about it, key techniques
4. Optionally update `templates/_index/` catalog

## Adding Moodboard Items

1. Drop files in the appropriate `moodboard/` subfolder
2. Add a companion `.md` file with notes on what's inspiring
3. Example: `moodboard/animations/vercel-ship-hero.gif` + `moodboard/animations/vercel-ship-hero.md`

## Adding Toolkit Patterns

1. Place in appropriate `toolkits/<lang>/<category>/`
2. File must be self-contained (works when copied standalone)
3. Header comment explaining what it does and usage example
4. Update the category's README.md if one exists

## When to Update Root Files

| Trigger | Action |
|---------|--------|
| New skill added | Update skills table in AGENTS.md + CLAUDE.md |
| New template source (not just template) | Update repo structure in AGENTS.md |
| Agent keeps getting confused | Refine the relevant skill or add clarification to AGENTS.md |
| Repo structure changes | Update the tree diagram in AGENTS.md |
