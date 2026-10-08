---
name: dev-project-session-manager
description: Worktree-first development environment — create per-issue or per-PR git worktrees, optionally with tmux sessions, so multiple work streams don't collide.
---

# Dev Project Session Manager

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Worktree-first development. Create per-issue or per-PR git worktrees so multiple work streams (different bugs, different features) don't collide on the same checkout.

## Use When
- Working on 2+ parallel branches that touch the same files
- Switching contexts often (review a PR while your own work is in progress)
- Long-running experiments that you don't want to disturb your main checkout

## Do Not Use When
- Single feature, single branch
- Project doesn't use git
- Disk space is tight (worktrees duplicate the working tree)

## Workflow

### Create
```bash
# Per issue
git worktree add ../{repo}-issue-123 -b issue/123-fix-auth

# Per PR (review)
git worktree add ../{repo}-pr-456 origin/feature/foo

# Per experiment
git worktree add ../{repo}-experiment-perf -b experiment/perf
```

### Optional: tmux session per worktree
```bash
tmux new-session -d -s {repo}-issue-123 -c ../{repo}-issue-123
```

### List
```bash
git worktree list
```

### Remove
```bash
git worktree remove ../{repo}-issue-123
git branch -d issue/123-fix-auth  # if merged
```

## Naming Convention
- `{repo}-issue-{N}` — issue work
- `{repo}-pr-{N}` — PR review
- `{repo}-experiment-{name}` — experiments
- `{repo}-hotfix-{name}` — urgent fixes

## Output
Save the active worktree map to `workspace/development/research/[C]worktrees-{date}.md`:

```markdown
## Active Worktrees — {date}

| Path | Branch | Purpose | tmux session |
|---|---|---|---|
| ../evo-ai-issue-123 | issue/123 | fix auth bug | evo-ai-issue-123 |
| ../evo-ai-pr-456 | origin/feat/x | review | (none) |
```

## Pairs With
- `@flow-git` (when worktrees need rebasing or commit splitting)
- Any agent that needs to work in isolation
