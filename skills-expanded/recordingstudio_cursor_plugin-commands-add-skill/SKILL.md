---
name: add-skill
description: Save a new skill into this Recording Studio Cursor plugin.
---

# Add a skill

Create a new skill in this plugin so it can be reused locally and published to the Cursor Marketplace.

Follow the `add-skill-or-agent` skill.

1. Ask for the skill name, when to use it, and the steps.
2. Add `skills/<name>/SKILL.md` with `name` and `description` frontmatter.
3. Make the folder name match the frontmatter `name`.
4. Run `node scripts/validate-plugin.mjs`.
5. Update `README.md` and `CHANGELOG.md`.
