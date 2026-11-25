---
name: github-ops
description: "GitHub operations: commit, push, PR, fix CI, address review comments. Replaces Codex github:github, github:gh-address-comments, github:gh-fix-ci, github:yeet. Use when user says 'push', 'create PR', 'fix CI', 'address comments', 'yeet', or needs Git/GitHub workflow help."
---

# GitHub Operations

Unified GitHub workflow skill for Claude Code. Covers the functionality of:
- `github:github` — repo, PR, issue management
- `github:gh-address-comments` — address PR review comments
- `github:gh-fix-ci` — diagnose and fix CI failures
- `github:yeet` — quick commit + push + draft PR

All operations use the `gh` CLI (GitHub CLI) and standard `git` commands.

## Commands

### /github-ops yeet
Quick ship: stage → commit → push → open draft PR.

1. `git status` to see changes
2. `git diff --staged` and `git diff` to understand changes
3. Stage relevant files (prefer explicit paths over `git add -A`)
4. Commit with a descriptive message
5. Push to remote with `-u` flag
6. `gh pr create --draft` with auto-generated title and body

### /github-ops fix-ci
Diagnose and fix CI/GitHub Actions failures.

1. `gh run list --limit 5` to find recent runs
2. `gh run view <id> --log-failed` to get failure logs
3. Analyze the failure (build error, test failure, lint issue, etc.)
4. Fix the root cause in code
5. Commit and push the fix
6. Verify with `gh run watch` if applicable

### /github-ops address-comments
Address PR review comments.

1. `gh pr view <number>` to get PR details
2. `gh api repos/{owner}/{repo}/pulls/{number}/comments` to get review comments
3. For each comment:
   - Read the referenced file and line
   - Implement the requested change
   - Stage the fix
4. Commit all fixes with a message referencing the review
5. Push to the PR branch

### /github-ops pr [action]
PR management.

- `create` — create PR with summary and test plan
- `view [number]` — view PR details and status
- `merge [number]` — merge PR (after checks pass)
- `list` — list open PRs

### /github-ops issue [action]
Issue management.

- `create` — create issue from description
- `view [number]` — view issue details
- `list` — list open issues
- `close [number]` — close issue with comment

## Rules

- Never force push without user confirmation
- Never skip hooks (--no-verify) without user confirmation
- Prefer specific file staging over `git add -A`
- Always include Co-Authored-By in commits when Claude Code writes the code
- Check `git status` before any destructive operation
