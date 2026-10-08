---
name: towles-tool
description: Use towles-tool (`tt`) CLI for journaling and worktrees. Use when asked about "tt commands", "daily notes", "meeting notes", or worktree management.
user_invocable: true
---

# towles-tool CLI

Personal CLI toolkit. Binary: `tt`

Config: `~/.config/towles-tool/towles-tool.settings.json`

## Journaling

```bash
tt journal daily-notes  # Weekly file, daily sections (alias: tt today)
tt journal meeting      # Meeting notes
tt journal note         # General notes
tt journal jot "text"   # Append a timestamped bullet to today's note
tt journal list         # Recent entries
tt journal search TEXT  # Search entries
```

## Open a path in the app

```bash
tt open src/main.rs        # reveal it in the app's Files pane, in *this* task
tt open src/main.rs:42     # …scrolled to line 42 (`--line 42` also works)
tt open crates/tt-git      # a folder opens the pane on that checkout
```

Shows the path in the running app's Files pane, beside the terminal you typed it
in — routed by the `TT_SESSION_ID` the app stamps on its terminals, so it lands
in this task's window and not another's. From a terminal the app didn't spawn
there's no session to route on and it falls back to the checkout the path is in.

Fails (non-zero), rather than opening anything else, when: the path doesn't
exist, it's under no git repository (the pane browses a checkout), or no app
instance is serving this checkout — there is no `preferredEditor` fallback.
`preferredEditor` still applies to the journal commands above.

## Worktree tasks

```bash
tt task init               # Onboard a repo: template, gitignore .env, primary .env
tt task new "Do the thing" --repo myrepo -b feat/thing  # board task + branch-named worktree + rendered .env
tt task new "Do the thing" --repo myrepo --goal "..."   # goal shown on the Board card under the title
tt task ls                 # Fleet: main checkout + tasks, branch, dirty, ports
tt task env <name>         # (Re)render a checkout's .env (or `primary`) — idempotent, keeps claims
tt task ports              # Repo's port picture: every checkout's claims + registry, each probed (`--probe <port>` for one)
tt task sync [<name>]      # Record the branch a task's worktree is on now (default: cwd's task)
tt task rm <name>          # Guarded removal
tt task clean              # Remove every merged/gone task
tt task nudge <prs|issues|slack:dm>  # Refresh that collector now instead of on the app's next poll
```

`nudge` is for hooks and scripts, not for you to run by hand — the app polls
these collectors on its own cadence anyway. It routes by `TT_SESSION_ID`, so
it reaches the app instance that opened the terminal it runs in; from a
session started outside the app it reaches every open instance. Add
`--only-if-tracked` and it skips — successfully — unless the terminal is one
the app spawned or the cwd sits under a repo on the rail, which is what keeps
a globally enabled hook from sweeping `gh` for unrelated projects.

Run `sync` (or the MCP `task_sync` tool) after creating or switching branches
inside a task's worktree: the board card records the branch the task was made
with, and PR auto-linking follows the record, not the checkout. The folder
keeps its name. It refuses a detached HEAD and the task's base branch.

`rm`/`clean` run a task's declared `TT_TASK_TEARDOWN` command (from its
rendered `.env`) against the worktree right before removing it — for
whatever a task's `TT_TASK_SETUP` started that the built-in docker
compose/container sweep can't find on its own (e.g. a compose stack not
named after the task). Unset by default; declare it per-repo in
`.env.example`.
