---
name: skill-validator
description: Validate a single Claude Code skill for correctness. Checks SKILL.md markdown formatting, YAML frontmatter fields (name, description, allowed-tools), and reviews skill content for consistency issues like mismatched permissions, undocumented arguments, and tools used but not listed. Use this skill whenever someone asks to validate, lint, or check a skill, verify a SKILL.md is well-formed, check if frontmatter is correct, audit allowed-tools or permissions, or catch problems before publishing a skill to a marketplace.
license: MIT
compatibility: Requires Node.js
allowed-tools: Bash, Read
argument-hint: <path-to-skill-directory>
metadata:
  author: jamessawle
  version: "1.0"
---

# Skill Validator

Validates a single Claude Code skill across three layers:

1. **Markdown formatting** — via markdownlint
2. **Frontmatter validation** — required fields and types
3. **Content review** — LLM-driven analysis of skill consistency

## Required permissions

Add this to your settings so the validation runs without prompts:

**Allow:**

```text
Bash(*/scripts/validate.sh*)
```

## Arguments

- `$0` — Path to a skill directory (containing `SKILL.md`). Defaults to the current working directory if not provided.

## Workflow

### Step 1: Verify target

Check that `$0/SKILL.md` exists. If not, report an error and stop.

### Step 2: Automated checks

Run markdown formatting and frontmatter validation:

```bash
${CLAUDE_SKILL_DIR}/scripts/validate.sh '$0'
```

This checks:

- Markdown formatting via markdownlint
- YAML frontmatter is present and parseable
- Required fields exist: `name`, `description`, `license`, `compatibility`, `metadata`
- `name` follows the naming convention: lowercase `a-z`, numbers, hyphens only; max 64 characters; no leading, trailing, or consecutive hyphens; must match the parent directory name
- `description` is non-empty and at most 1024 characters
- `license` is a non-empty string
- `compatibility` is a non-empty string, at most 500 characters
- `metadata` is a map of string key-value pairs
- Optional field `allowed-tools` is validated if present
- File paths referenced in SKILL.md content exist on disk — checks `${CLAUDE_SKILL_DIR}/...` paths, `references/...`, and `scripts/...` references relative to the skill directory

Report results but continue even on failure.

### Step 3: Content review

Read the `SKILL.md` and review:

- **allowed-tools consistency**: If `allowed-tools` is present in frontmatter, are all tools used in the workflow listed? Flag tools used but not listed. Also flag tools listed in `allowed-tools` that are never used in the workflow — recommend removing them to minimise the permission surface.
- **Permission pattern consistency**: If a "Required permissions" section exists, do the patterns match commands actually used in the workflow? Flag dead permissions (listed but never used) and uncovered commands (used but not listed).
- **Argument consistency**: Are `$0`, `$1`, etc. documented in an "Arguments" section and referenced in the workflow? Flag undocumented or unused arguments.
- **Command pattern coverage**: Are there commands in the workflow that would need user approval but aren't mentioned in the permissions section?

### Step 4: Summary

Output a combined report:

- **Markdown formatting**: X errors found (or "clean")
- **Frontmatter validation**: passed or failed with details
- **Content review**: findings or "No issues found"
- **Overall verdict**: PASS / FAIL with actionable next steps for any failures
