---
name: project-brief
description: Starts a new project note (a single file, or a folder with Brief, Current-State and Decisions) by interviewing the user for the why, scope and definition of done; or, for an existing project, loads its brief and current state and summarizes where things stand before any work begins. Use when the user says "start a project", "new project", "write a brief for X", "what's the status of X", "catch me up on X", "let's work on X", runs /project-brief, or when a task touches a project whose notes you have not read yet this session.
argument-hint: "[project name]"
---

# Project brief

First find out whether the project exists: Grep `Projects/` for the name (files and folder names, and `title`-like headings).

## Existing project: load it

1. Read `Brief.md` and `Current-State.md` (folder project), or the single project note.
   Skim `Decisions.md` headings and the last few meetings that link the project.
2. Summarize in the chat, in under ten lines: the goal, where things stand, next actions, open questions, anything blocked.
3. Point out anything that looks stale: `updated:` more than a month old while `status: active`, checked boxes still listed as next actions, a `Current-State` that contradicts a newer meeting note.
   Ask before fixing.

Then do the task the user came for.

## New project: create it

### 1. Interview (short)

- What is it, and why now?
- What is in scope, and what is explicitly out?
- How will you know it worked? Push for something checkable ("ten people use it", "the bed survives a season"), not "it's good".
- Who else is involved? (Link existing person notes.)
- The first two or three next actions.

### 2. Choose the shape

- **Single file** (`Projects/Name.md`) by default.
- **Folder** (`Projects/Name/Brief.md`, `Current-State.md`, `Decisions.md`) when the project will run for months, involve several people, or collect many decisions.
  A single-file project can be split into a folder later; offer that when one grows past a couple of screens.

### 3. Write it

- From `System/Templates/Project.md` (and `Project-Current-State.md` and `Decision.md` for the folder shape).
- Use the user's words for the why and the scope.
- Fill `created:` and `updated:` with today's date and set `status: active` (or `idea` if they are not starting yet).
- Add typed links where they apply (`works_with::`, `depends_on::`, `part_of::`).
- Run `python3 scripts/check_vault.py`, show the user the note, and commit if they have agreed to agent commits.
