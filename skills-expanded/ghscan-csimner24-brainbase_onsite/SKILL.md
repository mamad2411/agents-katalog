---
name: author-skill
description: How to write a new reusable skill (a markdown procedure) so future turns can follow it.
tools: [create_skill, list_skills, read_skill, list_tools]
---

# Author a skill

A skill is a short procedure in markdown that tells a future run of this agent how to do one job well. Write one when a task is likely to recur, took several steps to get right, or depends on preferences the user stated.

## Steps

1. Call `list_skills` first. If a similar skill exists, update it with `update_skill` instead of creating a near-duplicate.
2. Pick a slug name: lowercase, digits, `-` or `_` only (e.g. `weekly-report`). `create_skill` rejects duplicates and suggests `update_skill`.
3. Write a one-line `description` that says when to use it. It is shown in the skill index every turn, so make it specific.
4. Body structure:
   - `# Title`
   - `## When to use` (one or two lines)
   - `## Steps` (numbered, concrete, reference tool names in backticks)
   - `## Output` (what the finished result looks like, including file names and formats)
   - `## Pitfalls` (things that went wrong before and how to avoid them)
5. If the skill depends on a tool in this workspace, list it in `tools` and name it in the steps. If the tool does not exist yet, create it first (see `author-tool`).
6. Keep it under ~60 lines. Skills are procedures, not essays.
7. Never embed user file contents or personal data in a skill. Refer to inputs generically ("the uploaded PDF") and call `list_files` at run time.

## After creating

Tell the user the skill name and that they can run it with `/<name>`.
