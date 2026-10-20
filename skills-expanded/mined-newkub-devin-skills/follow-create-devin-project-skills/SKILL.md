---
name: follow-create-devin-project-skills
description: Standards for creating project-local Devin skills in .devin/skills/ per project conventions
argument-hint: "[skill-name...]"
related:
  - update-project-skills
  - update-devin-global-skills
  - update-dot-devin
  - update-devin
  - update-docs
  - review-devin-global-harness
  - scan-codebase
  - deep-validate

---

## Goal

Define the standard for creating project-local Devin skills in `.devin/skills/` — naming, structure, content rules, and syncing with the project's `AGENTS.md`

## Scope

Use as the primary reference when creating a new skill in a project or monorepo workspace's `.devin/skills/` — not for global skills in `%APPDATA%\devin\skills` (use `/update-devin-global-skills` instead)

See also: /update-project-skills, /update-devin-global-skills, /update-astgrep-rules, /update-agents-md

- Format: a Devin skill = `SKILL.md` as the entry point — no `references/` by default (merge content into `SKILL.md` per the conventions in `/update-devin-global-skills`; split files only with a clear reason, e.g. workflows/scripts) — confirm the latest format with `/deep-research` + `/follow-best-practice`

## Execute

### 1. Identify Skill And Workspace

> Goal: know which skill to create and in which workspace

1. Take `skill-name` from the argument or context — if unclear → run `/ask-me`
2. Identify the target: root `.devin/skills/` or `apps/<workspace>/.devin/skills/`
3. Verify the skill is truly project-specific — if it's generally useful → hand off to `/update-devin-global-skills`
4. Run `/scan-codebase` to find the project-specific workflows/patterns the skill will cover

### 2. Check Duplicates And Conventions

> Goal: no duplication with existing skills and matching conventions

1. Check the project's `.devin/skills/` and `%APPDATA%\devin\skills` for similar skills
2. Run `/review-devin-global-harness` or `/use-related-skills` if a possibly duplicate skill is found
3. Read the root and workspace `AGENTS.md` to extract project conventions, commands, and tech stack
4. Read the existing skills in `.devin/skills/` to pick a directory pattern and style consistent with the project

### 3. Create Structure

> Goal: the skill has a correct starting structure

1. Create `<project-or-workspace>/.devin/skills/<skill-name>/SKILL.md`
2. Use kebab-case and the frontmatter `name` must match the directory name
3. If code is needed → create `src/` per the project stack detected from the manifest
4. If more detail is needed → merge it into `SKILL.md` staying within 250 lines (no `references/` by default); if truly necessary use `workflows/` or `scripts/` instead
5. If there are enforceable conventions → use ast-grep rules in `rules/` per `/update-astgrep-rules` instead of embedding them in the skill

### 4. Write SKILL.md

> Goal: the skill document is correct per the project-side spec

1. Complete frontmatter: `name`, `description` ≤100 characters, `argument-hint`, `related`
2. Sections: `## Goal` → `## Scope` → `## Execute` → `## Rules` → `## Expected Outcome`
3. Write the content entirely in English, unless the project specifies another language
4. Use the project's real commands and paths from `package.json`, `AGENTS.md`, or existing scripts
5. Use backticks for `tools`, `commands`, `paths`, `skill-name`
6. Stay under 250 lines — compress details concisely into `SKILL.md` instead of splitting `references/`

### 5. Sync With Project

> Goal: the skill is wired into project artifacts

1. Run `/update-agents-md` so `AGENTS.md` references the new skill if it's a primary workflow
2. Check that `related` points to skills that really exist in both the project and global sets
3. If the skill concerns hooks/MCP → sync with `/update-devin-project-hooks` or `/update-devin-project-mcp`
4. Run `/update-dot-devin` if the `.devin/` manifest needs updating

### 6. Validate And Ship

> Goal: the skill passes the standard before delivery

1. Run `/deep-validate` — frontmatter, length, TODO/placeholder, broken links
2. Check that `related` has no missing or circular entries
3. If it fails → fix and recheck no more than 3 rounds
4. Hand off to `/update-project-skills` for later updates

## Rules

### 1. Project-Local Only

- Create only project-specific skills — for general skills use `/update-devin-global-skills`
- Don't duplicate existing global skills

### 2. English Content

- Project-local skills are written entirely in English
- Unless the project explicitly specifies another language

### 3. Naming And Structure

- `name` matches the directory name, kebab-case
- `description` ≤100 characters
- No file over 250 lines
- No TODO/MOCK/placeholder

### 4. Project Truth

- Use commands, paths, and conventions from the project's real `AGENTS.md` and manifests
- Don't hardcode commands that don't exist in the project
- Do a dry run before overwriting an existing skill and always ask for confirmation
- Use /update-docs when needed


## Expected Outcome

- The new skill lives in the correct project or workspace `.devin/skills/<skill-name>/`
- `SKILL.md` is in English and passes the frontmatter spec and section order
- Uses real project commands/paths, no duplication with global skills
- `AGENTS.md` and `.devin/` are synced correctly
- Passes `/deep-validate` and is ready to use
