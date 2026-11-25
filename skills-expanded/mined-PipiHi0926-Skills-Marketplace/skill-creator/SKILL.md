---
name: skill-creator
description: >
  Guide through creating a new Claude Code skill. Use when someone wants to build a
  new slash-command, create a SKILL.md, design a plugin, or learn the skill format.
  Triggered by: "create a skill", "new skill", "write a SKILL.md", "help me make a plugin".
argument-hint: "[skill-name] [brief description]"
allowed-tools: Read, Write, Glob
---

# Skill Creator

You are a specialist in Claude Code skill authoring. Guide the user to create a
well-formed SKILL.md following the official Agent Skills standard.

## Process

### Step 1: Gather requirements

Ask the user (if not already provided via $ARGUMENTS):
1. What is the skill name? (kebab-case, max 64 chars, becomes the /slash-command)
2. What does it do? (This becomes the description — front-load the key use case)
3. Should Claude trigger it automatically, or only when the user types /name?
4. Does it need specific tools? (Read, Write, Bash, Grep, etc.)
5. Does it take arguments? (e.g., /fix-issue 123)
6. Should it run in isolation from the conversation? (context: fork)
7. Are there side effects? (deploy, commit, send message → needs disable-model-invocation: true)

### Step 2: Explain key frontmatter decisions

Walk through the frontmatter fields relevant to their use case:

**`name`** (optional): Defaults to directory name. Use kebab-case, max 64 chars.

**`description`** (strongly recommended): Claude uses this to decide when to load
the skill automatically. Front-load the trigger: "Use when X" or "Triggered by: Y".
Keep it under 250 characters — longer descriptions are truncated in the skill listing.

**`disable-model-invocation: true`**: Use for skills with side effects (deploy,
commit, send message). Prevents Claude from deciding on its own to run them.

**`allowed-tools`**: Restricts which tools Claude can use without asking permission
when the skill is active. Good for read-only skills: `Read, Grep, Glob`.

**`argument-hint`**: Shows in autocomplete. Use `[arg]` for optional, `<arg>` for
required. Example: `[issue-number]` or `<filename> [format]`.

**`context: fork`**: Runs the skill in an isolated subagent. Use for tasks that
should not see conversation history, like deep research or code generation tasks.

**`effort`**: Override the session effort level. Options: low, medium, high, max.

### Step 3: Generate the SKILL.md

Produce a complete, ready-to-use SKILL.md. Structure the content as:

1. One-sentence purpose statement
2. Usage examples showing /skill-name invocation patterns
3. Step-by-step instructions Claude will follow
4. Output format specification (if applicable)

### Step 4: Recommend file placement

Explain where to place the skill:

| Goal | Path |
|------|------|
| Personal, all projects | `~/.claude/skills/<skill-name>/SKILL.md` |
| This project only | `.claude/skills/<skill-name>/SKILL.md` |
| Shared via this marketplace | `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` |

For marketplace distribution, also update:
- `.claude-plugin/marketplace.json` — add plugin entry with version
- `plugins/<plugin-name>/.claude-plugin/plugin.json` — plugin manifest (no version field for local-path plugins)

### Step 5: Validate

Check the generated SKILL.md against this checklist:
- [ ] `name` is kebab-case and under 64 characters
- [ ] `description` is under 250 characters and front-loads the trigger case
- [ ] `disable-model-invocation: true` is set for skills with side effects
- [ ] `$ARGUMENTS` is present in the content if the skill takes arguments
- [ ] Instructions in the body are actionable, not just descriptive
- [ ] Supporting files are referenced from SKILL.md if they exist

## Additional resources

See [reference.md](reference.md) for the complete frontmatter field reference
and [examples/example-skill.md](examples/example-skill.md) for a worked example.
