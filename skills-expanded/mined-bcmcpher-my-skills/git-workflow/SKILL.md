---
name: git-workflow
description: Auto-invoke when the user asks about committing changes, writing a commit message, creating or reviewing a pull request, branching, rebasing, resolving merge conflicts, or coordinating parallel agents with worktrees. Provides decision context and references for git operations in Claude Code sessions.
argument-hint: [describe task or ask about specific git operation]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash
---

# Git Workflow for Claude Code Sessions

Use this skill to reason about git operations before executing them. Read the
references for command sequences and conflict resolution details.

## Decision: Which git strategy to use

**In-place commits** — small, focused changes on the current branch:
- Single file or tightly coupled set of files
- Completing a step that is already in progress
- No risk of conflicting with other work

**Branches** — sequential tasks that need review before merging:
- New feature or bug fix that warrants a PR
- Work spanning multiple commits over time
- Naming convention: `kebab-case`, descriptive (e.g. `fix-auth-token-expiry`)

**Worktrees** — parallel independent tasks:
- Two or more agents working on unrelated parts of the codebase simultaneously
- Use `isolation: worktree` in agent frontmatter (see templates/agent)
- Each worktree gets its own branch; merged sequentially by dependency order
- See `${CLAUDE_PLUGIN_ROOT}/references/worktree-patterns.md` for lifecycle commands

## Commit conventions

- Subject line: imperative mood, ≤72 chars (e.g. `Add retry logic to upload handler`)
- Body: explain *why*, not *what* — the diff shows what
- Always include trailer: `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- One logical change per commit; don't bundle unrelated fixes

**Commit cadence:** Commit at the completion of each logical unit of work — a passing
behavior in TDD, a completed analysis phase, a reviewed chunk of a refactor. Don't
accumulate changes until a full feature is done; small commits make bisect and revert
precise. If using `/tdd`, each Red-Green-Refactor cycle is a natural commit boundary.

## Parallel agent coordination

1. Assign each agent its own branch (or use `isolation: worktree` for full isolation)
2. Agents should not share a working tree — race conditions on staged files
3. After agents finish, merge in dependency order (leaf changes first)
4. Prefer rebase over merge to keep history linear: `git rebase main`
5. Check for a common ancestor before merging: `git merge-base <branch> main`

## Conflict resolution

See `${CLAUDE_PLUGIN_ROOT}/references/conflict-resolution.md` for step-by-step
decision logic (rebase vs. merge vs. cherry-pick) and marker resolution patterns.

## Available commands

These commands execute the operations described above. Use them after deciding on the right strategy.

| Command | When to use |
|---|---|
| `/commit` | Stage and commit with a conventional message (Co-Author trailer included) |
| `/commit-push-pr` | Commit, push to origin, and open a GitHub PR in one step |
| `/review-pr [number]` | Review an open GitHub PR and post findings as a PR comment |
| `/clean-gone` | Remove local branches (and worktrees) deleted on the remote after merge |

## Constraints

- Always run `git fetch origin` before creating a new branch or worktree
- Never force-push to `main` or `master`
- Never commit secrets, `.env`, or credential files
- Always verify `git status` is clean before switching branches or starting a worktree
- Prefer `git mv` over bare `mv` for tracked files (enforced by git-guard.sh hook)
