---
name: git-github-general-repository-maintenance
description: Maintains Git and GitHub repositories safely. Use when inspecting repository state, planning branch hygiene, checking remotes, auditing local changes, preparing safe history repair, or guarding risky Git commands.
license: MIT
compatibility: Requires git for repository inspection; optional Python 3 for hook guard script and POSIX shell for the repository inspection helper.
---

# Git/GitHub Repository Maintenance

This skill helps agents keep Git repositories safe, understandable, and recoverable.

## When to Use This Skill

Use this skill for:

- repository state inspection;
- branch, remote, and upstream checks;
- local change audits;
- safe history repair planning;
- repository hygiene review;
- dangerous Git command evaluation;
- branch protection and repository policy recommendations.

## Operating Principles

1. Inspect before changing.
2. Prefer read-only commands until the desired operation is clear.
3. Preserve user work and unrelated local changes.
4. Treat history rewrites and destructive cleanup as exceptional.
5. Avoid secrets exposure in output.
6. Create a written plan before remote-changing operations.

## Suggested Read-Only Checks

Use project policy first. In a typical Git repository, useful checks include:

```bash
git status --short --branch
git remote -v
git branch --show-current
git branch -vv
git log --oneline --decorate --graph --max-count=20
git diff --stat
git diff --cached --stat
```

Do not paste sensitive diff content unless the user asked for it and the content has been reviewed for secrets.

## Scripts

Run scripts with `--help` before using them.

- `scripts/inspect-repo-state.sh` prints a safe, compact repository summary.
- `scripts/git-command-guard.py` is used by the plugin hook to classify risky Git commands.

## Workflows

- `workflows/repository-health-check-workflow.md`: Use before substantial repository operations, onboarding to an unfamiliar repository, or preparing a PR.
- `workflows/history-repair-workflow.md`: Use when the user asks to undo, revert, reset, rebase, force-push, remove commits, repair tags, or recover from a bad merge.

## Resources

- `resources/repository-health-checklist.md`
- `resources/branch-policy-template.md`

## Examples

- `examples/safe-history-rewrite-plan.md`
- `examples/protected-branch-settings.md`

## Decision Tree

- Need only understand state? Use read-only inspection.
- Need preserve public history? Prefer revert, merge, or a new corrective commit.
- Need change unpublished local commits? Consider amend, rebase, or reset only after saving state.
- Need modify remote history? Require explicit approval, backup refs, affected branch list, and rollback instructions.
- Need GitHub metadata changes? Prefer a draft or comment before changing labels, milestones, reviewers, branch protection, or merge state.
