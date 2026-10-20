---
name: follow-devin-global-skills
description: Read and use the skills available in global and project (.devin/skills) stores as appropriate
argument-hint: "[skill-name]"
related:
  - list-devin
  - search-skills
  - update-project-skills
  - check-reference
  - update-devin-global-skills
  - deep-validate
  - update-references
  - report
  - follow-up-to-date

---

## Goal

Read and use the skills available in both the global store (`%APPDATA%\devin\skills`) and the project store (`.devin/skills`) as appropriate for the current task

## Scope

- Find all skills available in the session
- Covers both global and project-level skills
- Read the chosen skill and follow its instructions
- Verify that references actually exist

## Execute

### 1. List Available Skills

> Goal: know which skills exist

1. Run `/list-devin-global-skills` to see global skills
2. If the project has `.devin/skills/`, list `.devin/skills/*` as well
3. If a project `AGENTS.md` exists, read its `### Skills` section
4. Build the `global` and `project` skill lists with paths

### 2. Map Skills To Task

> Goal: use a map to find skills faster

1. If `argument [skill-name]` is not given → run `/search-skills` to find skills matching the task
2. If several skills match → show the map and let the user choose

### 3. Resolve Skill Name

> Goal: locate the skill to use

1. If `argument [skill-name]` is given → find the exact skill
2. If not given → infer from the task context
3. Search both the global store and the project's `.devin/skills/`
4. If a global and a project skill share a name → use the project skill unless the global is newer or the user specifies

### 4. Read Skill

> Goal: understand the skill's content

1. Read the chosen skill's `SKILL.md`
2. If it has `references/`, read the relevant `.md` files
3. Identify goal, scope, execute, rules, expected outcome
4. Verify that every skill in `related` exists

### 5. Check References

> Goal: verify correctness before use

1. Run `/check-reference` to check references
2. If a reference does not exist → notify the user or use `/update-references`
3. Check the skill has no circular dependency
4. If the skill's content contains versions/APIs/commands — check freshness per `/follow-up-to-date` before trusting it

### 6. Use Skill

> Goal: carry out the skill

1. Follow the instructions in `## Execute`
2. Use the tools the skill specifies
3. If the skill says to use other skills → repeat `/follow-devin-global-skills` in order
4. Verify the results against `## Expected Outcome`

### 7. Report

> Goal: summarize skill usage

1. Run `/report` stating the skills used, results, and next action
2. If several skills were used → summarize the sequence

## Rules

### 1. Global + Project

- Search both global and project skills
- Project skills take priority on name collisions
- If nothing is found → tell the user and suggest creating one

### 2. Reference First

- Always read a skill before using it
- Check references before citing them
- Never use a skill that fails validation

### 3. Scope Respect

- Do not use unrelated skills
- Never dispatch duplicate skills
- Use `argument-hint` as the skill specifies

- Use /update-project-skills if needed
- Use /update-devin-global-skills if needed (devin global skills)
- Use /deep-validate if needed

## Expected Outcome

- Skills read and used correctly
- The skills applied fit the task
- All references are valid
- Results match expectations
