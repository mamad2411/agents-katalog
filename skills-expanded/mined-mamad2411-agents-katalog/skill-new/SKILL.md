---
name: skill-new
description: >-
  Scaffolds a new skill in the current project, following the project's
  existing skill layout.
when_to_use: >-
  Use when the user asks to create, add, or scaffold a new skill
  (e.g. "создай скилл", "новый скилл", "add a skill", "scaffold a skill").
---

# skill-new

Create a new skill folder with a properly formatted `SKILL.md`,
placed according to the current project's layout.

## When NOT to use

Triggers for activation live in the frontmatter `when_to_use` field.
Do NOT activate for editing existing skills —
only for creating new ones.

## Inputs to collect

Before writing files, make sure you have:

1. **`name`** — lowercase, hyphen-separated, unique among existing skills.
   Derive from the user's request if obvious;
   otherwise ask.
2. **`description`** —
   one or two sentences describing what the skill does.
   Keep it concise;
   trigger conditions go in `when_to_use`.
   Ask the user if unclear.
3. **`when_to_use`** —
   trigger conditions that tell the agent when to activate this skill:
   phrases the user might say, file types, project shapes.
   The agent matches against `description` + `when_to_use` combined,
   so be concrete.
   Ask the user if unclear.
4. **Body content** —
   the steps the agent should follow when the skill activates.
   Ask the user for the procedure if they haven't described it.

## Determine the target directory

Look at where existing `SKILL.md` files live in the project
and follow the same convention.
Common layouts:

- `skills/<name>/SKILL.md` — most common multi-skill repo
- `.claude/skills/<name>/SKILL.md` — Claude-specific project layout
- `<name>/SKILL.md` at repo root — flat layout

If no existing skills are found, default to `skills/<name>/SKILL.md`.

## Steps

1. Determine the target directory using the rule above.
2. Verify the target path does not already exist.
   If it does, stop and ask whether to overwrite or pick a different name.
3. Create the directory.
4. Write `SKILL.md` using the template below.
5. Report the created path.

## SKILL.md template

```markdown
---
name: <name>
description: >-
  <one or two sentences: what the skill does>
when_to_use: >-
  <triggers: phrases the user might say, file types, project shapes>
---

# <Human-readable title>

<One-paragraph summary of what the skill does.>

## Steps

1. <First action>
2. <Second action>
3. <Final action>
```

## Rules

- Don't add `scripts/` or `references/` subfolders
  unless the skill actually needs them —
  keep the scaffold minimal.
- Don't write a per-skill README;
  `SKILL.md` is the documentation.
- Frontmatter `name` must match the folder name.
