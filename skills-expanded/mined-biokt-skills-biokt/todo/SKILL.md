---
name: todo
description: View, add, complete, reorganize, or auto-update tasks in the project's TODO.md file. Use when tracking progress, adding new ideas, marking tasks done, or inferring completed tasks from conversation context.
allowed-tools: Read, Write, Edit, Glob
---

Manage the TODO.md file in the current working directory. Parse the optional argument `$ARGUMENTS` to determine what action to take.

## Format

TODO.md uses a flat markdown format with H1 for the project title and H2 sections for task categories. Tasks use GitHub-style checkboxes:
- `- [ ] task description` — pending
- `- [x] task description` — completed

Example structure:
```
# Project Name

## Category Name
- [x] Completed task
- [ ] Pending task
```

## Actions

### No argument or `show` — Display current TODO
Read TODO.md and show its full contents to the user in a clean, readable format. If the file does not exist, say so and offer to create it.

### `add <section>: <task>` — Add a new task
Add a pending task `- [ ] <task>` under the specified section. If the section does not exist, create it. If no section is specified, ask the user which section to add it to, listing existing ones.

### `done <task-description>` — Mark a task as complete
Find the task by matching the description (partial match is fine) and change `- [ ]` to `- [x]`. If multiple tasks match, list them and ask the user to clarify.

### `new <Project Name>` — Create a new TODO.md
Create a fresh TODO.md in the current directory with the given project name as the H1 title and a starter section. Warn if TODO.md already exists before overwriting.

### `section <name>` — Add a new section
Append a new H2 section with the given name at the end of the file (before any trailing blank lines).

### `clean` — Archive completed tasks
Move all `- [x]` items into a collapsible `## Done` section at the bottom, or remove them if a `## Done` section already exists and the user confirms. This keeps the active task list tidy.

### `update` — Auto-tick completed tasks from context
Read TODO.md, then review the current conversation context to infer which pending tasks have been completed. For each pending task (`- [ ]`) that the conversation clearly shows has been done, mark it as complete (`- [x]`). Be conservative: only mark tasks done when there is clear evidence in the conversation. After editing, list each task you ticked and briefly explain the evidence that justified it. If nothing is clearly done, say so rather than guessing.

## Rules

- Always operate on `TODO.md` in the **current working directory**.
- Preserve the existing structure and ordering of sections and tasks when editing.
- Do not reformat or reword existing task text.
- When the action is ambiguous or the argument is missing, read the file first and ask a targeted clarifying question rather than guessing.
- After any modification, briefly confirm what changed (e.g., "Added task to ## Simulations in water").
- Keep the file minimal — no extra blank lines between tasks, one blank line between sections.
