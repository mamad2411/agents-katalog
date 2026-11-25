---
name: antonify-skill-integrator
description: Install, adapt, or document Antonify as reusable agent skills for Claude Code, Codex, OpenClaw, Hermes Agent, and other SKILL.md-compatible agent tools. Use when the user asks to integrate Antonify, create platform-specific skill folders, write install instructions, package Antonify skills, or verify skill discovery paths.
---

# Antonify Skill Integrator

Use this skill when the task is about making Antonify usable inside another agent tool as a `SKILL.md`-based skill.

## Target Platforms

Support these common targets first:

- Claude Code: `.claude/skills` for project skills, `~/.claude/skills` for personal skills
- Codex: `.agents/skills` for repo skills, `~/.agents/skills` for personal skills
- OpenClaw: workspace `skills/` or `~/.openclaw/skills`
- Hermes Agent: `~/.hermes/skills` or `skills.external_dirs` in `~/.hermes/config.yaml`

For other tools, use the portable pattern: a folder with `SKILL.md`, optional `references/`, optional `scripts/`, and optional `assets/`.

## Workflow

1. Identify the target agent platform and whether the skill should be repo-scoped, workspace-scoped, or personal.
2. Choose the Antonify skill to install or adapt.
3. Keep the skill folder name and the `name` field in `SKILL.md` aligned.
4. Copy only the needed skill folder, not the whole repo, unless the target tool needs the full reference set.
5. Add or update platform-specific install instructions.
6. Add a test prompt that should trigger the skill.
7. Verify the skill has valid frontmatter and a clear trigger description.

## Skill Folder Rules

- Every installable skill must have a top-level `SKILL.md`.
- Put the most important trigger words early in `description`.
- Keep platform-specific setup notes out of the main instruction skill unless they affect how the agent performs the task.
- Use `references/` for longer platform details, examples, and install notes.
- Avoid duplicating the full Antonify docs inside each skill.

## Output Expectations

When documenting an integration, include:

- Target platform
- Install location
- Copy command or setup steps
- Invocation or test prompt
- Any restart, reload, or discovery command
- Link back to `docs/agent-skill-integration.md` when this repo is available

When creating files, prefer this structure:

```text
skills/
`-- skill-name/
    |-- SKILL.md
    `-- references/
        `-- optional-reference.md
```

## Validation

Before finishing, check:

- `SKILL.md` exists at the root of each skill folder.
- Frontmatter has `name` and `description`.
- The `name` matches the folder name.
- The description says when the skill should trigger.
- Install instructions point to the correct platform directory.
- Test prompts match the actual skill behavior.
