---
name: autogit-integration
description: Auto stage → commit → push for Hermes Agent + OpenCode using autogit CLI
version: 1.2.0
author: the operator
license: MIT
metadata:
  hermes:
    tags: [git, automation, ci, devops, version-control, hooks]
    triggers: [autogit, auto-commit, auto-push, git, ship, commit, push]
    related_skills: [vcs-management]
---

# Autogit Integration

When you make meaningful changes to any git repository on this system, you MUST run `autogit ship` afterward. This triggers the auto-commit-and-push pipeline.

## How It Works

- **autogit** is installed globally (`npm i -g @davidondrej/autogit` v0.6.0)
- Wired agents: **Claude Code**, **Codex CLI**, **Cursor**, **Pi** (via lifecycle hooks)
- **OpenCode** shares Codex hooks (`~/.codex/hooks.json`)
- Hermes integration: this skill + a periodic watchdog cron job

## Repos with autogit Enabled

These repos auto-push after every agent turn:

| Repo | Path | Notes |
|------|------|-------|
| hermes-config | `${MY_REPOS}/Documents/github/hermes-config/` | Config + nightly reports |
| agent-fleet | `${MY_REPOS}/Documents/github/agent-fleet/` | Gateway runner + teams |
| tor-browser-mcp | `${MY_REPOS}/Documents/github/tor-browser-mcp/` | Public fork, opted with --public-ok |
| mattpocock-skills | `${MY_REPOS}/Documents/github/mattpocock-skills/` | Public clone, opted with --public-ok |

## AGENTS.md Commit Discipline

Autogit commit discipline is documented in ~30 AGENTS.md files across all active repos. Every AGENTS.md carries:

```markdown
### Autogit & Commit Rules
- autogit (davidondrej/autogit v0.6.0) installed and auto-enabled on this repo
- Every meaningful change MUST be committed and pushed
- Descriptive commit messages, push at checkpoints, never leave uncommitted changes
- Always pull latest before starting work in a repo
```

When working in ANY repo, follow this pattern:
1. `git pull` (or `autogit status` to check state)
2. Make changes
3. `autogit ship` (or `git add -A && git commit -m "msg" && git push`)
4. Push at natural checkpoints: feature complete, bug fixed, refactor done, EOD

## For New Repos

```bash
cd /path/to/repo
autogit on            # enable auto-push
# or if public repo:
autogit on --public-ok
```

## Commands

```bash
autogit ship          # stage, scan secrets, commit, push
autogit undo          # take back last autogit commit
autogit status        # check hooks + repo state
autogit off           # disable auto-push in current repo
```

## Reference Files

| File | What it covers |
|------|---------------|
| `references/installation-setup.md` | Full implementation transcript — exact commands, file paths, verified behavior |
| `references/cron-timeout-fix.md` | Pattern for fixing 600s cron timeouts by converting LLM-driven jobs to no_agent scripts |
| `references/windows-cron-scripts.md` | Windows backslash path workaround — no_agent scripts must be .py not .sh |

## Workflow

1. You make changes via terminal()/write_file()/patch() in a git repo
2. Run `autogit ship` from the repo root (or let the hook fire on agent stop)
3. autogit stages all changes, scans for secrets, commits with a descriptive message, and pushes

## Watchdog (Cron Safety Net)

A no-agent cron job runs every 30 minutes to catch changes the hooks missed:
- Script: `~/.hermes/scripts/autogit-watchdog.py`
- Iterates every opted-in repo, checks `git status --porcelain`, runs `autogit ship` if dirty
- Uses full absolute paths for the autogit binary and `shell=True` for subprocess (Windows cron context has no npm/bin PATH)
- Stays silent when everything is clean

> **Windows quirk:** no_agent cron scripts must be `.py`, not `.sh`. The scheduler's path resolution uses `AppData\Local\hermes\scripts\` with backslashes that get stripped when passed to bash. Python subprocess handles the path correctly. See `references/windows-cron-scripts.md` for details.

## Safety

- Secret scanning blocks commits containing API keys, tokens, `.env` files, private keys, JWTs
- `--force-secrets` overrides the scan (but never puts secrets in commit subjects)
- **Log files with JWTs get blocked** — gateway logs in agent-fleet contain JWTs. Add them to `.gitignore` or use `--force-secrets`. The scan is intentional.
- `autogit undo` reverses the last autogit commit (local + remote)
- Parallel-agent aware — if another agent is mid-turn, autogit defers
- Nothing changed = nothing ships (no noisy empty commits)

## Pitfalls

- **Codex/OpenCode trust required** — after `autogit setup`, open OpenCode and run `/hooks` to trust autogit entries. Changes to `~/.codex/hooks.json` silently un-trust until re-confirmed.
- **OpenCode shares Codex hooks** — same binary lineage. No separate setup needed.
- **Cursor hooks run from ~/.cursor** — `ship` parses stdin JSON for `workspace_roots` to find the real project directory.
- **Public repo commit messages** — agent prompts become public commit subjects on public repos. `autogit on` warns; use `--public-ok`.
- **Secrets scan blocks JWTs in log files** — either `.gitignore` log dirs or pass `--force-secrets`.
- **Multi-account GitHub** — with multiple `gh` accounts, `autogit on` asks which to pin. Pass `--account <name>`.
- **Windows cron: no_agent scripts must be .py not .sh** — the scheduler resolves relative script paths using `~/AppData\Local\hermes\scripts\` as the base. The backslashes in the path get consumed as escape characters when passed to bash, mangling the path (e.g. `C:\Users\...` becomes `C:Users...`). Python scripts work because Python's subprocess handles the full path correctly. When calling system binaries (autogit, gbrain, etc.) from these Python scripts, use full absolute paths and `shell=True` since the cron context has a minimal PATH.
