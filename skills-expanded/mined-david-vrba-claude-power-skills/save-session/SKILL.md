---
name: save-session
description: Save current session state to project memory (session_state_[topic].md), discoverable via /catch-up and /resume. Archives stale states; keeps MEMORY.md uncluttered.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Save session

Save the current session state to the project's memory folder so a future
session — or `/catch-up` / `/resume` — can pick the work back up with zero
context loss. Follow these steps exactly.

## Step 1 — Locate the memory folder

Claude Code stores per-project memory under:

`~/.claude/projects/[encoded-path]/memory/`

Derive `[encoded-path]` from the current working directory by replacing every
`\`, `:`, and `_` character with `-`.

Example: `C:\Users\you\projects\my_app` → `C--Users-you-projects-my-app`

If memory files were already loaded this session, their paths in the
system-reminders reveal the folder directly — use that instead of recomputing.

## Step 2 — Run cleanup (archive stale session states)

Scan all `session_state_*.md` files currently in the memory folder (not in
`archive/`).

For each file found:
1. Read the `created:` field from its frontmatter.
2. Calculate calendar days since `created`.
3. If the adjusted age is greater than 7 days → move the file to
   `memory/archive/` (create the folder if needed with `mkdir -p`), then remove
   its line from `MEMORY.md`.

## Step 3 — Determine the session state filename

Check if a `session_state_[topic].md` already exists in the memory folder for the
same project or topic as this session.

- If yes → **overwrite it** (do not create a new file alongside it).
- If no → create `session_state_[topic].md` where `[topic]` is either the project
  name or a short slug that distinguishes this session's focus
  (e.g., `api_refactor`, `auth_bugfix`, `db_migration`).

## Step 4 — Write the session state file

Use this exact template:

```
---
name: Session State — [Topic] ([today's date])
description: [One sentence: what was worked on and current status]
type: project
created: [today's date as YYYY-MM-DD]
---

# Session State — [Topic] — [today's date]

## What We Were Working On
[2-4 sentences: the specific task, why it was being done, where things stood when the session ended]

## What's Done
[Bullet list of completed items. Include filenames and specifics. If nothing was coded, say "Design only" or "Planning only".]

## What Still Needs to Be Done

### Immediate (start here next session)
- [ ] [Max 5 items — specific enough to act on without rereading anything]

### Short-term
- [ ] [Items for this week]

### Longer-term / Backlog
- [ ] [Real but not urgent]

## Current Status
[2-3 sentences. Assume the reader has zero context. End with the single most important next action.]

## Key File Locations (if relevant)
| What | Path |
|---|---|
| [component] | [path] |
```

## Step 5 — Keep MEMORY.md clean (do NOT index session states)

Do **not** add a pointer line for this session state. `MEMORY.md` is auto-loaded
into every session in this folder; indexing parked task-state there bleeds
unrelated work into new sessions and invites hallucination. Session states are
pull-on-demand — `/catch-up` Globs the folders directly and `/resume` uses the
session-resume system; neither needs `MEMORY.md`.

- Remove any existing `session_state_*` lines from `MEMORY.md` (this supersedes
  any old "add a pointer" behavior).
- Also remove lines for any files you archived in Step 2.
- Leave durable memories (user / feedback / reference / active-checkpoint
  entries) untouched.

## Step 6 — Confirm

Say: "Session state saved: `session_state_[topic].md` — [one-line summary of what
was captured]. [N] file(s) archived."
