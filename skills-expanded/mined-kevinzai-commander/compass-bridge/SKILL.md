---
name: compass-bridge
description: |
  Shared state bridge between Claude Chat, Cowork, and Code. Uses markdown files at
  ~/.claude/compass/ as the synchronization layer. Tasks and state persist across all
  Claude surfaces without needing a database or MCP server.
triggers:
  - /compass
  - /sync-state
  - compass bridge
  - cross-surface sync
  - shared state
---

# Compass Bridge

A cross-surface synchronization layer that keeps tasks and session state consistent between Claude Chat, Claude Cowork, and Claude Code. Uses plain markdown files as the shared state -- no database, no MCP server, no external service.

## Architecture

Two files in `~/.claude/compass/` form the synchronization layer:

- **tasks.md** -- Shared task list. Any Claude surface can add, complete, or update tasks.
- **state.md** -- Session state. Tracks what is being worked on, where, and what is blocking progress.

Create the directory if it does not exist:

```bash
mkdir -p ~/.claude/compass
```

## tasks.md Format

```markdown
# Shared Tasks

<!-- Updated: 2026-03-28T14:30:00Z -->

## Active
- [ ] Build login page | priority:high | surface:code | created:2026-03-28
- [ ] Write onboarding copy | priority:medium | surface:chat | created:2026-03-28
- [ ] Review color palette | priority:low | surface:cowork | created:2026-03-27

## Completed
- [x] Set up project structure | surface:code | completed:2026-03-28
- [x] Define user personas | surface:chat | completed:2026-03-27
```

Each task line follows this format:
```
- [ ] {description} | priority:{high|medium|low} | surface:{code|chat|cowork} | created:{YYYY-MM-DD}
```

Completed tasks move to the `## Completed` section with a `completed` timestamp replacing `created`.

## state.md Format

```markdown
# Session State

<!-- Updated: 2026-03-28T14:30:00Z -->

## Current Focus
Building the authentication flow for the web app.

## Active Surface
code

## Blockers
- Waiting on API key for the email service (asked user 2026-03-28)

## Recent Context
- Decided on better-auth over next-auth for the auth library (simpler API, fewer dependencies)
- Database schema finalized: users, sessions, accounts tables
- Frontend using shadcn/ui components with Tailwind v4

## Last Updated
2026-03-28T14:30:00Z
```

## Operations

### add_task

Add a new task to the active list. Detect the current surface automatically (code, chat, or cowork based on the environment).

1. Read `~/.claude/compass/tasks.md` (create with template if missing)
2. Append new task to the `## Active` section
3. Update the `<!-- Updated: -->` timestamp
4. Write the file back

### complete_task

Mark a task as done.

1. Read `~/.claude/compass/tasks.md`
2. Find the matching task in `## Active` (match by description substring)
3. Change `[ ]` to `[x]`
4. Move the line to `## Completed` with a `completed` timestamp
5. Update the `<!-- Updated: -->` timestamp
6. Write the file back

### get_tasks

Read and display the current task list. Filter by status (active, completed, all) or priority.

1. Read `~/.claude/compass/tasks.md`
2. Parse and display in a clean format
3. Show counts: total active, by priority, recently completed

### update_state

Update the session state with current focus, blockers, or recent context.

1. Read `~/.claude/compass/state.md` (create with template if missing)
2. Update the relevant section(s)
3. Set `## Active Surface` to the current surface
4. Update `## Last Updated` timestamp
5. Write the file back

### get_state

Read and display the current session state. Useful at session start to understand what was happening on another surface.

1. Read `~/.claude/compass/state.md`
2. Display a formatted summary:
   ```
   Compass State

     Focus:    Building the authentication flow
     Surface:  code (last updated 2h ago)
     Blockers: 1 (API key pending)
     Context:  3 recent decisions
   ```

## Cross-Surface Workflow

### Starting a New Session

When a session starts on any surface:

1. Check if `~/.claude/compass/state.md` exists
2. If it does, read it and display a brief summary: what was last being worked on, which surface, any blockers
3. Check `~/.claude/compass/tasks.md` for active tasks
4. Offer to continue from where the last session left off

### During a Session

- After completing a significant task, update both files
- When the user makes a decision that affects other surfaces, add it to the `## Recent Context` section of state.md
- When new work items emerge, add them to tasks.md

### Ending a Session

Before the session ends:

1. Update state.md with current focus and any new context
2. Mark completed tasks in tasks.md
3. Add any new tasks that emerged

## Compatibility

This format is designed to be compatible with Rich Lira's Compass MCP server. If the user has Compass MCP installed, this skill reads and writes the same files. Both can coexist: the MCP server provides programmatic access while this skill provides conversational access.

## Guidelines

- **Always read before writing.** Never overwrite the file without reading it first. Another surface may have updated it since the last read.
- **Preserve existing content.** When updating, merge changes -- do not replace the entire file.
- **Timestamps matter.** Always update the `<!-- Updated: -->` comment so other surfaces know when the file was last modified.
- **Keep state.md concise.** The `## Recent Context` section should hold 5-7 items maximum. Older context rolls off as new items are added.
- **Task descriptions are the key.** Matching is done by description substring, so descriptions should be specific enough to be unique.
