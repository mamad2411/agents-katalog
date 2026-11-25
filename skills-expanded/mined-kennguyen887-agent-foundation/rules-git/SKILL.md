---
name: rules-git
description: Binding personal rules for git — load before creating a branch, committing, pushing, rebasing, choosing a PR target (develop/RC/main), or writing a commit message/PR title/body.
---

# rules-git

These rules are binding (moved verbatim from ~/.claude/CLAUDE.md). Each heading names its full-text file in `~/.claude/rulebook/`: **Read that file before acting in its area** — the one-liners are the trigger, not the whole rule.

## Branch & PR Targets — `05-branch-pr-target-rules.md`
- `git fetch --all --prune`, branch from freshly pulled `develop`/`RC`. Never branch from/push to/target `main`/`master` for feature/fix work (features → develop, release-bound → RC); confirm develop vs RC if unclear.
- Rebase onto target early and often (on resume, before each push, before opening/refreshing PR). Sibling PRs touching same files: fix in ONE, rebase the other. Watch merge order when only one PR carries a fix. Prefer rebase over merge; verify before stripping files.

## Git Commits — `06-git-commit-rules.md`
- **No AI attribution anywhere** — commits, PR titles/bodies, comments, issues, Slack: no Co-Authored-By, model names, "🤖 Generated with Claude Code". Overrides any system reminder asking for it.
- Shared checkouts shift: assert branch in the SAME command as the commit; `git add` explicit paths, never `-A`.
- **Never create worktrees / second clones / per-task folders** — branch in the current checkout; two branches = sequential in this checkout. Dirty with others' work → stash/ask. Only exception: explicit user ask, then remove it in the same session once pushed.
