---
name: mem-sync
description: Synchronize project daily memory logs (.memories/) across devices over Git using an isolated per-user branch and worktree, without polluting the active development branch. Use to pull other devices' logs at session start and push local logs at session end.
---

# mem-sync — Cross-Device Memory Sync

Synchronizes `<repo>/.memories/` across machines through a dedicated, isolated
per-user branch `memories/<email-localpart>` using a background git worktree, so the
active development branch and your editor workspace are never disturbed.

## Per-User Branch

The sync branch is derived from `git config user.email`: the part before `@`,
lowercased and slugified (non-alphanumeric runs become `-`). `User@Example.com` →
`memories/user`. Each user pushes/pulls only their own branch, so two developers on
the same repo never collide on same-date log filenames.

## Commands

Discover the script path dynamically (do NOT hardcode):
1. Global scope: `~/.agents/skills/mem-sync/scripts/mem-sync-git.sh`
2. Project scope: `<repo>/skills/mem-sync/scripts/mem-sync-git.sh`
3. Fallback: search for `mem-sync-git.sh`.

- `mem-sync-git.sh pull` — record local WIP, fetch+rebase remote, copy back. Run at session start.
- `mem-sync-git.sh push` — same merge, then push. Run at session end or after promoting candidates.
- `mem-sync-git.sh` (no argument) — defaults to `status`.
- `mem-sync-git.sh status` — read-only: fetch the per-user branch and summarize how local `.memories/` differs (in sync, or local-only / remote-only / modified files).
- `mem-sync-git.sh diff` — read-only: like `status` but prints the full unified diff (local vs remote).
- `mem-sync-git.sh print-branch` — print the derived per-user branch and exit (used by tooling/tests).
- `mem-sync-git.sh print-remote` — resolve and print the sync remote (env → config → auto-detect) and exit; use it to confirm which remote a sync would target. Exits non-zero with guidance if the remote is ambiguous.

See [references/git-sync-workflow.md](references/git-sync-workflow.md) for mechanics,
anti-pollution rules, and conflict handling.

## Remote resolution

The sync remote is resolved in this order:

1. **`MEM_SYNC_REMOTE` env var** — explicit one-off override; highest priority, never persisted.
2. **`git config memsync.remote`** — a persisted per-repo choice.
3. **Auto-detect** from the local remote list:
   - exactly one remote → use it (not persisted);
   - `origin` plus exactly one other remote → pick the non-`origin` one (this is the fork
     case where `origin` is an upstream you cannot push to);
   - two non-`origin` remotes, or more than two remotes → **ambiguous**: the command lists
     the remotes and exits non-zero. Choose one with `git config memsync.remote <name>`
     (persistent) or `MEM_SYNC_REMOTE=<name>` (one-off), then rerun.

After a successful `push`/`pull`/`compact` that used the two-remote auto-pick, the chosen
remote is written to `git config --local memsync.remote`, so later sessions skip detection.
A wrong remembered value is corrected with a single `git config memsync.remote <name>`.
The per-user branch name (`memories/<email-localpart>`) is unaffected by the remote choice.

If a command reports an ambiguous remote set, relay the printed remote list to the user and
ask which remote to use, then set `git config memsync.remote <name>` before retrying.

## Anti-Pollution

Never commit `.memories/` to an ordinary development branch. If the user asks to
"commit memory" or "sync daily notes to Git", intercept and route through this syncer.
