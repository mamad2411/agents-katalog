---
name: codex
description: "Use when delegating to OpenAI Codex CLI for coding tasks, permissioned validation/build runs, PR review, batch issue work, or visible interactive sessions; keep commits, pushes, PRs, and unsafe modes behind explicit user permission."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    related_skills: [claude-code, hermes-agent]
---

# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes terminal. Codex is OpenAI's autonomous coding agent CLI.

## Choose the Codex branch

- **Coding delegation** — hand Codex a bounded implementation/refactor/fix and review its diff before reporting success.
- **Permissioned validation** — use Codex as a build/test runner only after scope and command boundaries are explicit.
- **PR review** — ask Codex to inspect a diff or PR, then verify and summarize findings yourself.
- **Visible session** — use tmux/Windows Terminal only when the user needs to watch or interact with Codex directly.

Completion requires the Codex process to exit or be intentionally killed, the resulting diff/logs to be reviewed by Hermes, tests/builds to be independently verified where practical, and the user to receive changed files, commands run, and remaining risks.

## Permission gates

- Do not use `--yolo`, `--dangerously-bypass-approvals-and-sandbox`, or equivalent unsafe modes unless the user explicitly authorizes them for the current workspace.
- Do not commit, push, create PRs, post comments, or merge unless the user explicitly asks for that side effect.
- Prefer scoped prompts that name allowed paths and forbidden actions.
- If Codex asks a question or proposes a risky action, stop and route the decision back through Hermes/user approval.

## When to use

- Building features
- Refactoring
- PR reviews
- Batch issue fixing

Requires the codex CLI and a git repository.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials
  from the Codex CLI login flow
- **Must run inside a git repository** — Codex refuses to run outside one
- Use `pty=true` in terminal calls — Codex is an interactive terminal app

For Hermes itself, `model.provider: openai-codex` uses Hermes-managed Codex
OAuth from `~/.hermes/auth.json` after `hermes auth add openai-codex`. For the
standalone Codex CLI, a valid CLI OAuth session may live under
`~/.codex/auth.json`; do not treat a missing `OPENAI_API_KEY` alone as proof
that Codex auth is missing.

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For scratch work (Codex needs a git repo):
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

When using Codex to exercise an installed skill and return an artifact to the user:
1. Create a temporary git repo (`mkdir`, `git init`) because Codex requires one.
2. Put the user's brief in a file so Codex has stable context.
3. Run `codex exec --full-auto 'Use $skill-name ... create <artifact>'` with `pty=true`.
4. Monitor with `process.wait`/`poll`; if the artifact appears and Codex lingers, it is safe to kill the process after confirming the output file exists.
5. Verify/render the artifact yourself before sending it back.

Example:
```
terminal(command="mkdir -p ~/tmp-skill-demo && cd ~/tmp-skill-demo && git init && printf '%s\n' '<brief>' > brief.md && codex exec --full-auto 'Use $ian-xiaohei-illustrations. Read brief.md and create a sendable PNG or SVG artifact.'", background=true, pty=true)
```

## Background Mode (Long Tasks)

```
# Start in background with PTY
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Permissioned Validation via Codex

When the user explicitly says Codex has permissions/access that Hermes lacks, use Codex as a validation runner rather than stopping at local tool limitations. Keep the task narrow and evidence-focused:

```
codex exec --full-auto 'Run the focused build/test for <target>. Do not modify source files. Return exact commands, pass/fail results, and errors.'
```

Operational pattern:
1. Start Codex in a PTY background session and monitor with `process.wait`/`process.log`.
2. Ask Codex to discover canonical repo scripts/resolvers before assuming paths.
3. If Codex discovers the needed command/path but hangs or drifts into broad discovery, kill it after capturing the command and run the focused command yourself.
4. Verify success from the underlying tool logs/output, not only from Codex's self-report.
5. If tests are newly added/generated, build the relevant target first; otherwise test registration may fail even though the test source exists.
6. For Unreal/S2 build validation, see `references/unreal-build-validation.md`: Codex sandbox may block UBT log/intermediate writes, so rerun narrowly with `--yolo` only when authorized, keep `Do not edit files or commit` in the prompt, and watch for UHT shadowing errors like reflected `Owner`/`Role` parameters on `AActor` subclasses.


## Visible Windows Terminal / tmux Sessions

When the user asks to *see* a Codex session on the Windows host, prefer a real visible Windows Terminal window/tab if tmux cannot create a durable pane. Use native Windows paths for visible terminals:

```
powershell.exe -NoProfile -Command "Start-Process wt -ArgumentList @('-d','C:\\Users\\Admin\\project','cmd.exe','/k','codex')"
```

If attempting `tmux-windows`, verify the session remains alive before reporting success:

```
tmux -L codex new-session -d -s codex-project 'cmd.exe /k cd /d C:\\Users\\Admin\\project'
tmux -L codex list-sessions
```

Pitfalls:
- A `tmux new-session` command can return success while the Windows shell exits immediately; always follow with `tmux list-sessions` or `capture-pane`.
- MSYS/bash paths are fine for non-UI Hermes terminal commands, but `wt`/`cmd.exe` arguments should use native `C:\\...` paths.
- If tmux pane creation fails, do not stop at the failure; open `wt` directly so the user can still see and interact with Codex.

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Rules

1. **Always use `pty=true`** — Codex is an interactive terminal app and hangs without a PTY
2. **Git repo required** — Codex won't run outside a git directory. Use `mktemp -d && git init` for scratch
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly
4. **`--full-auto` for building** — auto-approves changes within the sandbox
5. **Background for long tasks** — use `background=true` and monitor with `process` tool
6. **Don't interfere** — monitor with `poll`/`log`, be patient with long-running tasks
7. **Parallel is fine** — run multiple Codex processes at once for batch work
