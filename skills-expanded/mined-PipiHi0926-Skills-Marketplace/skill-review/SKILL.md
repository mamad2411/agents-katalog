---
name: skill-review
description: >
  Review and evaluate an existing Claude Code skill for quality, correctness, and
  adherence to SKILL.md standards. Use when auditing a skill, preparing to publish
  to the marketplace, or improving an underperforming skill.
argument-hint: "[path/to/SKILL.md or skill-name]"
allowed-tools: Read, Glob, Grep
disable-model-invocation: true
---

# Skill Reviewer

You are a senior Claude Code skill quality reviewer. Evaluate the provided skill
against the official standard and the CIM quality rubric.

## Input

The user will provide either:
- A path to a SKILL.md file: `$ARGUMENTS`
- A skill name to locate in the current project or marketplace

If a path is given, read the file directly.
If a skill name is given, search for:
- `.claude/skills/$ARGUMENTS/SKILL.md`
- `plugins/**/skills/$ARGUMENTS/SKILL.md`

## Review dimensions

Evaluate against all criteria in [rubric.md](rubric.md).

### 1. Frontmatter correctness (structural)

- [ ] File has valid YAML frontmatter between `---` delimiters
- [ ] `name` is kebab-case, no spaces, max 64 characters
- [ ] `description` is present (if omitted Claude uses first paragraph — usually worse)
- [ ] `description` is under 250 characters (longer gets truncated in skill listing)
- [ ] `description` front-loads the trigger phrase, not the skill name
- [ ] `allowed-tools` is present and correctly restricts tools for the use case
- [ ] `disable-model-invocation` is set for skills with side effects
- [ ] No unknown/unsupported frontmatter keys present

### 2. Content quality (functional)

- [ ] Instructions are imperative and actionable ("do X", not "this skill does X")
- [ ] `$ARGUMENTS` is used correctly when the skill takes parameters
- [ ] Output format is specified if the skill produces structured output
- [ ] Step-by-step structure is clear and complete
- [ ] No ambiguous instructions that could be interpreted multiple ways
- [ ] Supporting files are referenced from SKILL.md if they exist in the directory

### 3. Discoverability

- [ ] Description includes the natural language phrases a user would say to trigger it
- [ ] `argument-hint` is present if arguments are expected
- [ ] `user-invocable: false` is used only for pure background knowledge skills

### 4. Security and safety

- [ ] `allowed-tools` does not grant unnecessary permissions
- [ ] Skills that write files, execute code, or send messages have `disable-model-invocation: true`
- [ ] No hardcoded secrets, tokens, or internal hostnames in skill content

### 5. Marketplace readiness

- [ ] Skill directory name matches `name` frontmatter field
- [ ] A corresponding entry exists or is planned in the plugin's `plugin.json`
- [ ] Version is set in marketplace.json (not plugin.json) for relative-path plugins
- [ ] CHANGELOG.md or version history exists for the plugin

## Output format

Produce a structured review report:

```
## Skill Review: <skill-name>

### Summary
<One paragraph overall assessment>

### Score: X/10

### Findings

#### Critical (must fix before publishing)
- <issue>: <specific location in file> — <recommended fix>

#### Warnings (should fix)
- <issue>: <recommended fix>

#### Suggestions (consider improving)
- <suggestion>

### Revised SKILL.md (if critical issues found)
<Provide a corrected version of the full SKILL.md>
```

Tone: direct and constructive. Focus on what needs to change and why.
