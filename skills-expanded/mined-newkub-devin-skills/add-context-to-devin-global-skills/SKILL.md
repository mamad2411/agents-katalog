---
name: add-context-to-devin-global-skills
description: Capture context from a session or user, then add it to an existing global skill or create a new one
argument-hint: "<context-or-prompt>"
allowed-tools:
  - read
  - write
  - edit
  - grep
  - find_file_by_name
  - exec
  - skill
  - run_subagent
  - ask_user_question
  - todo_write
triggers:
  - user
  - model
related:
  - list-devin
  - new-skills
  - update-devin-global-skills
  - use-related-skills
  - review-devin-global-harness
  - idea
  - list-devin-session
  - ask-me
---

## Goal

Take context from a session, a user prompt, or learned information, then decide which global skill to add it to or whether to create a new skill.

## Scope

Use when the user wants to save context, knowledge, patterns, workflows, or recently discussed information into `%APPDATA%\devin\skills`, preferring additions to existing skills and creating new ones only when nothing fits.

## Execute

### 1. Capture Context

> Goal: Capture and summarize the context to add

1. If the user passed an argument, run `/list-devin-session` to pull session context, then run `/ask-me` to ask which item they mean.
2. Take input from the user, such as a context summary, keyword, topic, prompt, or a recap of what was discussed.
3. If the input is a link/URL, fetch or scrape it to summarize the title and description.
4. If the input is broad or unclear, ask the user what they want to save.
5. If there is no input, summarize the latest context from the session.

### 2. List Existing Skills

> Goal: Find skills that may be a good fit

1. Run `/list-devin-global-skills` to see the existing skills.
2. Run `/use-related-skills` to find related skills.
3. Use `grep` to search for skills related to the context, case-insensitively.
4. Read the 2-4 most relevant skill files.
5. Check `description`, `scope`, and `related` to judge the fit.

### 3. Decide Placement

> Goal: Decide where to place the context

1. If the context is about a tool/library/framework → target the skill with the matching name.
2. If the context is a broad topic/guide → consider adding to `related` or `references/`.
3. If the context is a workflow/pattern → add it to the skill with the matching domain.
4. If the context is a new skill candidate → create a new skill.
5. If the context duplicates an existing skill → stop and tell the user.

### 4. Add To Existing Skill

> Goal: Add the context to an existing skill

1. Open the chosen skill's `SKILL.md`.
2. If the context is another skill's name, add it to `related`.
3. If it is a URL/resource, add it to `references/` or `links`.
4. If it is a requirement/step, add a bullet under `Execute` or `Rules`.
5. Use `edit` or `write` carefully without breaking the frontmatter.
6. Verify the frontmatter is correct.

### 5. Create New Skill

> Goal: Create a new skill when nothing fits

1. If the context matches no skill at all, ask the user whether to create a new one.
2. If the context comes from a session pattern, run `/idea-devin-global-skills-from-session`.
3. If the user agrees, use `/new-skills` or `/update-devin-global-skills`.
4. Name the skill to match its directory name and keep `description` ≤ 100 characters.
5. Fill in `related` completely.

### 6. Verify

> Goal: Check correctness

1. Re-read the edited skill to check the references.
2. Run `/review-devin-global-harness` to check for duplicate/missing `related` entries.
3. Run `/review-devin-global-harness` if multiple skills were changed.
4. Run `/update-references` if any skill was created/removed/moved.

## Rules

- Prefer adding context to existing skills before creating a new one.
- Never add duplicate references.
- Don't change a skill's `name` or `description` unless necessary.
- If the context contains a secret/token, refuse and tell the user to store it in a secret manager.
- If the context is a URL, fetch and summarize it before deciding.
- When unsure, ask the user before making changes.
- If a new skill must be created, double-check before creating it.

## Expected Outcome

- The context is added to the appropriate skill.
- The user knows where the context lives and why.
- Any newly created skill passes conventions and validation.
