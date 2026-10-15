---
name: notis-skill-creator
description: Guide for creating effective skills. Use when users want to create a new skill that extends the assistant's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Notis Skill Creator

This skill guides the process of creating new skills from scratch or iterating on existing ones. A skill is a self-contained unit of instructions, references, and optional scripts that extend the assistant's capabilities.

## When to Use This Skill

- User wants to create a new skill (e.g., "Create a skill for X", "I need a skill that does Y")
- User is iterating on or packaging an existing skill
- User asks how to structure, validate, or distribute a skill

## Skill Development Workflow

### Step 1: Define the Skill

Before creating files, clarify:

- **Name** — kebab-case (e.g., `my-skill`, `api-helper`)
- **Description** — One or two sentences: what the skill does and when to use it
- **Scope** — Instructions only, or instructions + scripts/references/assets

### Step 2: Plan the Contents

- **SKILL.md** — Required. Contains YAML frontmatter (`name`, `description`) and the main instructions.
- **scripts/** — Optional. Executable code (Python, Bash, etc.) the assistant can run.
- **references/** — Optional. Documentation or reference files loaded on demand.
- **assets/** — Optional. Templates, images, or other files used in outputs.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

When creating a new skill from scratch, create the directory structure manually:

```bash
mkdir -p my-skill/scripts my-skill/references my-skill/assets
```

Then create `my-skill/SKILL.md` with the proper YAML frontmatter:

```markdown
---
name: my-skill
description: "Description of what this skill does and when to use it"
---

# My Skill

## Instructions

(Add your skill instructions here)
```

Create any supporting files in the appropriate directories:

- `scripts/` for executable code (Python, Bash, etc.)
- `references/` for documentation to be loaded on demand
- `assets/` for files used in output (templates, images, etc.)

### Step 4: Writing and Iterating

- Keep instructions clear and actionable. Include when to use the skill, required inputs, and expected outputs.
- Reference scripts or assets by path (e.g., `scripts/helper.py`, `references/glossary.md`).
- Test the skill by having the assistant follow it in a real scenario.

### Step 5: Save the Skill in Notis

When the user wants a Notis skill created, saved, or updated, save it directly in Notis by default. Do not make the user manually download and upload a zip unless they explicitly ask for an export.

For a simple skill that only needs a `SKILL.md`:

1. Finish the `SKILL.md` content.
2. Call `notis_create_skill` with:
   - `name`
   - `description`
   - `skill_md`

For a multi-file skill that needs `scripts/`, `references/`, or `assets/`:

1. Build the skill folder locally.
2. Package it into a zip:

```bash
cd /path/to/parent && zip -r my-skill.zip my-skill/
```

3. Wait for Notis to surface the generated file's public URL in the shell/file context.
4. Call `notis_create_skill` with:
   - `name`
   - `description`
   - `bundle_url`

Before saving, validate your skill:

- `SKILL.md` exists with proper YAML frontmatter (`name` and `description` fields)
- Skill name follows kebab-case (lowercase letters, digits, and hyphens)
- Description clearly explains what the skill does and when to use it

Only hand the zip file back to the user when they explicitly ask for the bundle itself.

## SKILL.md Frontmatter

Every skill must have a SKILL.md with at least:

```yaml
---
name: skill-name
description: "Clear description of what the skill does and when to use it."
---
```

- **name** — kebab-case identifier; used for packaging and display.
- **description** — Shown in skill lists and used for triage; be specific.

## Best Practices

1. **One clear purpose** — Each skill should do one thing well.
2. **Good description** — The description is used to decide when to invoke the skill; make it searchable and precise.
3. **Stable structure** — Use `scripts/`, `references/`, `assets/` consistently so users and tools know where to find things.
4. **Validate before packaging** — Check frontmatter, naming, and that all referenced files exist.

## Notis-Specific Notes

- Notis should save new skills directly with `notis_create_skill` whenever possible.
- Zip bundles are still valid internally, but they should usually be passed back into Notis through `bundle_url`, not handed to the user for manual upload.
- The Notis repo stores only Notis-specific skills under `skills/`; other skills (e.g., from Anthropic) are synced from their sources.
- When Notis Desktop Sync is enabled in the Electron app, skills created via `notis_create_skill` are automatically pulled to `~/.agents/skills/` and symlinked to local agents (Claude Code, Cursor, Codex). Conversely, skills created locally in `~/.agents/skills/` are auto-pushed to the Notis portal. No manual sync step is needed.
