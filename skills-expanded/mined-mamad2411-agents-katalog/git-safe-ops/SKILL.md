---
name: git-safe-ops
description: Encodes safe git operation rules — no force-push to main, always branch, always review before merge.
category: mcp
tags: [git, safety, devops, version-control]
agents: [opencode, freebuff, antigravity, codex]
---

# git-safe-ops

This skill is the standing safety contract for all git operations. It is **always-on** — load it in every coding, homelab, and documentation session where any git command may be executed.

## Purpose

Prevent irreversible or destructive git actions. Enforce branching discipline, review gates, and credential hygiene across all repositories in the pvnkmnk ecosystem.

## Invocation

**OpenCode / Codex:** `Invoke git-safe-ops`
**Freebuff:** `/skill git-safe-ops`

## Core Safety Rules

1. **Never force-push to main or master.** `git push --force` on a protected branch is forbidden. Use `--force-with-lease` on feature branches only, and only when you understand what you are overwriting.
2. **Always work on a branch.** No direct commits to `main` or `master` unless the repo is explicitly configured for trunk-based development and the user confirms.
3. **Review before merge.** Open a PR or at minimum run `git diff main` and confirm the changeset with the user before merging.
4. **Commit messages must be descriptive.** No `fix`, `update`, `wip` without context. Format: `type: short summary\n\nOptional body.`
5. **Credentials never in commits.** No API keys, tokens, passwords, or `.env` files with real values committed to any branch. Check with `git diff --staged` before committing if credentials are in scope.
6. **No bulk deletes without confirmation.** `git clean -fdx`, `git reset --hard`, and branch deletion require explicit user confirmation.
7. **Tag releases.** Any deployment or release commit should be tagged (`git tag -a vX.Y.Z`).
8. **Stash before switching.** If work-in-progress exists, stash before checking out another branch.

## Escalation Rules

Stop and confirm with the user if:
- The operation affects the default branch of any repository.
- A `--force` flag is being considered.
- More than 5 files would be deleted or reset.
- A merge conflict resolution is ambiguous.
- A `.env`, `secrets.*`, or credential file is within the staged changeset.

## Inputs

- Target repository and branch name
- Proposed git command(s) and intent
- Optional: commit message draft for review

## Outputs

- Reviewed, safety-checked git command(s) ready to execute
- Commit message conforming to the format convention
- Confirmation of branch state before and after the operation

## Failure Modes

- Pre-commit hook blocks commit — surface hook output to user; do not bypass hooks silently.
- Merge conflict on pull — list conflicting files; do not auto-resolve; present options to user.
- Remote history diverged — never silently force-push; present `git log --oneline origin/branch..HEAD` to user for review.

## References

- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

## Companion Skills

- `homelab-safe-ops` — infrastructure safety gate (parallel always-on)
- `tdd-loop` — commit discipline during test-driven development
- `refactor-with-tests` — branching discipline during refactor sessions
- `memory-layer-bridge` — log significant repo decisions to Obsidian
