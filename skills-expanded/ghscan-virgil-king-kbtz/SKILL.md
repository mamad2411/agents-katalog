---
name: kbtz-basics
description: This skill should be used when the user asks about "kbtz commands", "task tracking", "how to use kbtz", "create a task", "add a note", "list tasks", "task dependencies", or needs a reference for kbtz CLI usage.
---

# kbtz Task Tracker Reference

## Commands

| Command | Description |
|---------|-------------|
| `kbtz add <name> <desc> [-p parent] [-c assignee] [-n note] [--agent type] [--paused]` | Create a task |
| `kbtz claim <name> <assignee>` | Claim a task |
| `kbtz claim-next <assignee> [--prefer text]` | Atomically claim the best available task |
| `kbtz steal <name> <assignee>` | Atomically transfer task ownership (requires user approval) |
| `kbtz release <name> <assignee>` | Release a claimed task |
| `kbtz done <name>` | Mark task complete (requires user approval first) |
| `kbtz reopen <name>` | Reopen a completed task |
| `kbtz pause <name>` | Pause a task (remove from active work and default listing) |
| `kbtz unpause <name>` | Unpause a paused task (return to open) |
| `kbtz describe <name> <desc>` | Update a task's description |
| `kbtz reparent <name> [-p parent]` | Change a task's parent (omit -p to make root-level) |
| `kbtz rm <name> [--recursive]` | Remove a task (--recursive to remove children) |
| `kbtz list [--status S] [--json] [--tree] [--all] [--root name] [--children name]` | List tasks |
| `kbtz show <name> [--json]` | Show task details and blockers |
| `kbtz note <name> [content]` | Add a note to a task (reads stdin if content omitted) |
| `kbtz notes <name> [--json]` | List notes for a task |
| `kbtz block <blocker> <blocked>` | Set dependency (blocker must finish before blocked can start) |
| `kbtz unblock <blocker> <blocked>` | Remove a blocking relationship |
| `kbtz agents` | List configured agent types |
| `kbtz watch [--root name]` | Launch interactive TUI |
| `kbtz wait` | Block until database changes |

## Task Naming

Task names must be **kebab-case**: lowercase letters, numbers, and hyphens only. Names are immutable — they cannot be changed after creation, so choose carefully.

## Session ID

Use `$KBTZ_SESSION_ID` as your assignee in all kbtz commands. This environment variable is set automatically by Claude Code.

```bash
kbtz claim my-task $KBTZ_SESSION_ID
```

## Never Release Your Own Task

**Do not use `kbtz release` on your own task.** Releasing makes the task unclaimed, which causes the workspace to spawn a new session for it — duplicating work and losing your context.

Instead:

- **Blocked or stuck?** → Ask the user for guidance.
- **Done?** → Clean up your session first (add notes capturing progress, remove temp resources, clean up worktrees), then call `kbtz done <name>`. This ends your session, so always add notes before calling it.
- **Waiting on child tasks?** → `kbtz wait` to block until the database changes, then check children's status. This does not end your session.

## Workspace sessions

When running inside `kbtz-workspace`, the workspace automatically creates
sessions for all open tasks. **Do not use `--claim` or `kbtz claim` when
creating tasks inside a workspace** — the workspace will claim and assign
sessions to new tasks automatically. Using `--claim` bypasses the workspace's
session management and creates ghost tasks that appear active without a
workspace session.

Only use `--claim` / `kbtz claim` outside of a workspace (e.g. standalone
CLI usage).

## Common Patterns

### Creating tasks

Keep descriptions to one sentence — they display in a single-line list view.
Put detailed context in a `-n` note so the task and its context are created
atomically:

```bash
kbtz add parent-task "Top-level description." -n "Detailed context, requirements, and acceptance criteria."
```

Outside a workspace, use `-c $KBTZ_SESSION_ID` to create and claim in one step:

```bash
kbtz add my-subtask "Short description." -p parent -c $KBTZ_SESSION_ID -n "Detailed context for the subtask."
```

Use `kbtz exec` when you need multiple commands in one transaction (e.g.
creating subtasks with blocking relationships):

```bash
kbtz exec <<'BATCH'
add child-one "First subtask." -p parent-task -n "Details for first subtask."
add child-two "Second subtask." -p parent-task -n "Details for second subtask."
block child-one child-two
BATCH
```

### Quoting in `kbtz exec`

`kbtz exec` uses its own quoting rules — not POSIX shell quoting.

**Double quotes** delimit strings. Inside double quotes, `\"` produces a
literal `"` and `\\` produces a literal `\`. All other characters
(including newlines) are literal.

**Single quotes and apostrophes** are ordinary characters — they do NOT
start quoted strings. `it's` and `don't` work without escaping.

**Heredocs** (`<<DELIMITER`) work like shell heredocs and are the best
way to include multi-line or complex text:

```
add my-task "Description" -n <<NOTE
Any content here — quotes, apostrophes, special characters.
No escaping needed inside a heredoc body.
NOTE
```

**Multiline double-quoted strings** are supported — a quoted string can
span multiple lines:

```
add my-task "Description" -n "First line
second line
third line"
```

**Recommendation:** For note content with any special characters, prefer
heredocs over double-quoted strings. Heredocs require no escaping at all.

Use `--paused` to create a task that shouldn't be worked on yet:

```bash
kbtz add deferred-task "Not ready yet" --paused
```

### Agent types

The workspace supports multiple agent backends (e.g., claude, gemini). Tasks use the workspace default unless overridden with `--agent`:

```bash
kbtz agents                    # list available agent types
kbtz add gemini-review "Review the design doc." --agent gemini
```

Only use `--agent` when a task specifically needs a non-default backend.

### Specifying closure conditions

When creating a task, clearly state the **closure condition** — what must happen before the task is considered done — in the description or an initial note. **Agents must never call `kbtz done` without explicit user approval.** There are two closure paths depending on the repository:

- **Repo with remote:** Create a PR, wait for CI to pass, and display the diff. Wait for the user to review. The user will either request changes or ask you to merge. Only call `kbtz done` after the user approves and the PR is merged.
- **Repo without remote:** Work in a worktree, then present the branch diff to the user. Wait for the user to review. The user will either request changes or ask you to merge to main. Only call `kbtz done` after the user approves and the branch is merged.

Examples:

```bash
kbtz add update-deps "Update outdated dependencies" -n "Close after user approves and PR is merged."
kbtz add fix-parser "Fix CSV parser edge case" -n "Close after user approves and branch is merged to main."
```

### Adding progress notes

```bash
kbtz note my-task "Investigated root cause, found X"
kbtz note my-task "Fix applied, running tests"
```

### Managing dependencies

```bash
# child-two cannot start until child-one finishes
kbtz block child-one child-two
```

**Session suspension:** When your task becomes blocked (either because you set up a blocking relationship or because another agent blocks you), your session will be suspended. A new session will be spawned when the task becomes unblocked. Before blocking your task, always:

1. Add notes capturing your current progress, decisions made, and enough context for a fresh session to resume the work.
2. Clean up running processes, temp files, or other resources.

```bash
kbtz note my-task "Progress: implemented X, Y remains. Next step: finish Y after blocker resolves."
kbtz block blocker-task my-task
```

### Viewing task tree

```bash
kbtz list --tree          # open tasks in tree form
kbtz list --tree --all    # include completed tasks
```

### Listing direct children

```bash
kbtz list --children my-task        # direct children only (depth 1)
kbtz list --children my-task --all  # include done/paused children
```

### Transferring task ownership

`steal` requires user approval before use. It atomically transfers an active task to a new assignee:

```bash
kbtz steal my-task $KBTZ_SESSION_ID
```
