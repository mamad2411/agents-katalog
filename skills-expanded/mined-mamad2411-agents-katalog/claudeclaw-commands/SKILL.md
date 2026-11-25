---
description: List, view, or invoke a Claw skill.
argument-hint: "[list|view <name>|run <name>]"
---

# Skill command

Parse `$ARGUMENTS`:

- `list` (or no args) — List every skill in `${CLAUDE_PLUGIN_ROOT}/skills/` as `name — one-line description` (pull the description from each `SKILL.md` frontmatter).

- `view <name>` — Print the full `SKILL.md` for that skill.

- `run <name>` — Invoke the skill via the `Skill` tool with `skill: <name>`.

- `new <name>` — Scaffold a new skill: create `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md` with the standard frontmatter template (name, description) and ask the user three questions: (1) what trigger phrases should activate it, (2) what's the procedure, (3) what's the output format. Fill those into a clean SKILL.md.
