---
name: organize-commits
description: Organize uncommitted changes or messy commits on the current branch into clean, categorized commits grouped by purpose.
argument-hint: "[base-branch]"
---

## Context

Current branch: !`git symbolic-ref --short HEAD 2>/dev/null || echo "(detached HEAD or no commits yet)"`
Base branch (arg `$1`, falls back to `origin/HEAD` then `main`): !`echo "${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)}"`
Upstream: !`git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || echo "(no upstream tracked)"`
Ahead / behind upstream: !`git rev-list --left-right --count '@{upstream}...HEAD' 2>/dev/null | awk '{print "behind "$1", ahead "$2}' || echo "(n/a)"`

### Uncommitted changes

!`git status --short`

### Commits on this branch vs base

!`(BASE="${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)}"; git log --oneline "$(git merge-base HEAD "$BASE" 2>/dev/null)..HEAD" 2>/dev/null) || echo "(no committed history yet — empty repo or no merge-base with $BASE)"`

### Diff stat: committed vs base

!`(BASE="${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)}"; git diff --stat "$(git merge-base HEAD "$BASE" 2>/dev/null)..HEAD" 2>/dev/null) || echo "(no committed diff to show)"`

### Diff stat: uncommitted vs HEAD

!`git diff --stat HEAD 2>/dev/null || git diff --stat --cached 2>/dev/null || echo "(no HEAD yet — working tree below is the entire initial set)"`

## Instructions

Analyze all changes (committed + uncommitted), group by **purpose**, and create clean commits. **Always print the categorization plan first; pause for confirmation before any destructive operation** (`git reset`, anything that requires force-push to publish).

### Scenarios

1. **No HEAD (empty repo)**: stage and commit; the first commit becomes the initial commit. Do not reset.
2. **Uncommitted only**: stage and commit into categorized groups; existing commits stay as-is.
3. **Existing commits to reorganize, all local**: `git reset --soft <base>` to collapse into the index, then re-commit by category.
4. **Existing commits to reorganize, some already pushed**: same as #3, but `ahead` is non-zero against upstream so the rewritten branch can only be published with force-push. Surface this in the plan and require explicit confirmation.
5. **Both uncommitted and existing commits**: same flow as #3 or #4.
6. **Detached HEAD**: stop. Ask the user to check out a branch first (`git switch -c <name>`); do not commit on a detached HEAD.

### Process

1. **Plan**: print one line per planned commit — `<conventional-prefix>(<scope>): <subject> — <file count> file(s)` — and list which files go in each. State the scenario number above.
2. **Confirm (only when destructive)**: for scenarios 3, 4, 5, ask before running `git reset`. For scenario 4 specifically, call out "rewriting N pushed commit(s); publishing requires force-push" so the user understands the consequence.
3. **Execute**: `git reset --soft <base>` if needed, then `git add <files>` + `git commit` per group. Stage by explicit paths; avoid `git add -A` and `git add .` so sensitive files (`.env`, credentials) don't sneak in.
4. **Verify**: `git status` is clean, then `git log --oneline -<n>` to show the rewritten tip.
5. **Recommended sanity check**: run the project's `build` / `test` if it's quick. A reordered history that no longer builds is the most common regression of this skill.

### Rules

- As many commits as the work has distinct concerns, no more. Resist over-splitting — a single-file polish change is fine as one commit.
- Use conventional commit prefixes: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`, `ci:`, `build:`, `chore:`, `revert:`.
- Group files by their primary concern. A single file may be split across commits with `git add -p` only when its diff genuinely spans two unrelated concerns; cohesive diffs stay together.
- Order: foundational (config, rename, types) → features → polish (docs, tests, chore).
- If pre-commit hooks fail, fix the issue and re-commit. Never use `--no-verify`.
- Match the repository's existing commit-message style (subject case, scope notation, body wrap, sign-off) — read recent `git log` if unsure.
- NEVER force push without explicit user permission, even when the rewrite would otherwise leave the branch unpublishable. State the situation and let the user run the force-push themselves.
