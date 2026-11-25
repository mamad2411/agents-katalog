---
name: coding-agent
description: >-
  Orchestrate Claude Code (or other coding agents) as background processes for
  non-interactive work. Use for batch PR reviews, parallel issue fixing with git
  worktrees, or any multi-agent coding task. Prefer background mode over
  interactive sessions for programmatic control.
metadata:
  version: "0.1.0"
  attribution: "adapted from steipete/agent-skills (coding-agent)"
---

# Coding Agent (background-first)

Use **bash background mode** for non-interactive coding work. For interactive
sessions, use tmux.

## Core pattern: workdir + background

```bash
# Create isolated workspace
SCRATCH=$(mktemp -d)

# Launch agent in scoped directory
bash workdir:$SCRATCH background:true command:"claude \"Your task\""
# Returns sessionId

# Monitor
process action:log sessionId:XXX
process action:poll sessionId:XXX

# Send input if agent asks a question
process action:write sessionId:XXX data:"y"

# Kill if needed
process action:kill sessionId:XXX
```

**Why `workdir` matters:** agent starts in a focused directory and doesn't
read unrelated files. Scope the working directory to only what the task needs.

## Claude Code

```bash
bash workdir:~/project background:true command:"claude \"Your task\""
```

Non-interactive flag (`--print` / `-p`) for one-shot output:
```bash
bash workdir:~/project background:true command:"claude -p \"Summarize src/\""
```

## Parallel PR reviews with git worktrees

For reviewing multiple PRs in parallel without branch conflicts:

```bash
# Fetch all PR refs
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# One agent per PR — no checkout conflicts
bash workdir:~/project background:true command:"claude \"Review PR #86. git diff origin/main...origin/pr/86\""
bash workdir:~/project background:true command:"claude \"Review PR #87. git diff origin/main...origin/pr/87\""

# Monitor all
process action:list

# Post results
process action:log sessionId:XXX
gh pr comment <PR#> --body "<review content>"
```

**Never checkout branches for parallel reviews** — `git diff` the refs directly
so agents don't conflict.

## Parallel issue fixing with git worktrees + tmux

For fixing multiple issues in parallel with full isolation:

```bash
# 1. Clone to temp location
cd /tmp && git clone git@github.com:user/repo.git repo-worktrees
cd repo-worktrees

# 2. One worktree per issue
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# 3. tmux sessions
SOCKET="${TMPDIR:-/tmp}/fixes.sock"
tmux -S "$SOCKET" new-session -d -s fix-78
tmux -S "$SOCKET" new-session -d -s fix-99

# 4. Launch agent in each
tmux -S "$SOCKET" send-keys -t fix-78 "cd /tmp/issue-78 && claude 'Fix issue #78: <description>. Commit and push.'" Enter
tmux -S "$SOCKET" send-keys -t fix-99 "cd /tmp/issue-99 && claude 'Fix issue #99: <description>. Commit and push.'" Enter

# 5. Monitor
tmux -S "$SOCKET" capture-pane -p -t fix-78 -S -30

# 6. Check done (prompt returned)
tmux -S "$SOCKET" capture-pane -p -t fix-78 -S -3 | grep -q "❯" && echo "Done!"

# 7. Create PRs
cd /tmp/issue-78 && git push -u origin fix/issue-78
gh pr create --repo user/repo --head fix/issue-78 --title "fix: ..." --body "..."

# 8. Cleanup
tmux -S "$SOCKET" kill-server
git worktree remove /tmp/issue-78
git worktree remove /tmp/issue-99
```

**Why worktrees over branches:** each agent works in isolated branch, no
conflicts. Scales to 5+ parallel fixes.

**Why tmux over bash background for interactive agents:** tmux provides a TTY
for agents that need interactive output. Use bash background for one-shot tasks,
tmux for long-running sessions.

## Rules

1. **Respect tool choice** — if user asks for a specific agent, use it
2. **Be patient** — don't kill sessions because they're slow
3. **Monitor with `process:log`** — check progress without interfering
4. **Parallel is fine** — run many agents at once for batch work
5. **Never review PRs in the live project directory** — clone to `/tmp` or use
   git worktree; checking out branches in a running project can break it
