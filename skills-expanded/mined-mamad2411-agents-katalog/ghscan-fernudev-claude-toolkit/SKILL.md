---
name: toolkit-create-skill
description: Scaffold a new Claude Code skill interactively
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(mkdir *), Write, Edit
argument-hint: "[skill-name]"
---

# Skill Scaffolding Wizard

Help the user create a new Claude Code skill by gathering requirements and generating the `SKILL.md` file.

## Process

### Step 1 - Gather requirements

Ask the user the following (use a single AskUserQuestion call when possible):

1. **Name** - If `$ARGUMENTS` is provided, use it as the skill name. Otherwise ask.
2. **Purpose** - What should this skill do? Ask for a one-sentence description.
3. **Invocation mode** - Should it be:
   - Manual only (`/name`) - for side effects like commits, deploys, messages
   - Auto + manual - Claude can also trigger it when the request matches
4. **Scope** - Where should it live:
   - Project (`.claude/skills/`) - shared via the repo
   - Personal (`~/.claude/skills/`) - only for this user

### Step 2 - Design the skill

Based on the answers, determine:

- **`name`**: lowercase, hyphens only, max 64 chars
- **`description`**: clear, specific - this controls auto-invocation
- **`disable-model-invocation`**: `true` if manual-only
- **`allowed-tools`**: only the tools the skill actually needs
- **`argument-hint`**: if the skill accepts arguments
- **`context`**: `fork` if the skill does heavy research/exploration
- **Instructions body**: step-by-step process, rules, examples

### Step 3 - Review existing skills

Read the existing skills in `.claude/skills/` and `~/.claude/skills/` to:
- Avoid name collisions
- Follow consistent formatting patterns
- Reuse good conventions from existing skills (like the `/commit` skill)

### Step 4 - Generate the SKILL.md

Create the directory and `SKILL.md` file. Follow this template structure:

```markdown
---
name: <name>
description: <clear one-liner>
disable-model-invocation: <true|false>
allowed-tools: <comma-separated list>
argument-hint: "<hint>"
---

# <Title>

<Brief description of what this skill does.>

## Process

1. Step one...
2. Step two...
3. Step three...

## Rules

- Constraint one
- Constraint two

## Examples

<Concrete examples of expected input/output>
```

### Step 5 - Confirm and create

Show the user the full `SKILL.md` content before writing it. After approval:

1. Create the directory at the chosen scope
2. Write the `SKILL.md` file
3. Tell the user how to invoke it: `/skill-name`

## Quality Checklist

Before finalizing, verify:

- [ ] `name` is lowercase with hyphens, no spaces
- [ ] `description` is specific enough to avoid false auto-triggers
- [ ] `disable-model-invocation: true` is set for anything with side effects
- [ ] `allowed-tools` follows least privilege (no `Write` for read-only skills)
- [ ] Instructions are explicit, step-by-step, with concrete examples
- [ ] No name collision with existing skills

## Rules

- Always show the full SKILL.md content to the user before writing
- Never overwrite an existing skill without explicit confirmation
- Keep instructions concise - under 150 lines in the body
- Include at least one concrete example in every skill
- Reference the guide at `docs/skills.md` if the user wants to learn more
