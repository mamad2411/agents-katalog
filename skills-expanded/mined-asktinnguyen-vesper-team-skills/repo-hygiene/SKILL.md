---
name: repo-hygiene
description: Audit and clean git repo hygiene across branches and worktrees. Use when the user asks for git/worktree hygiene, stale branch cleanup, merged cleanup, conflict review, or a repo hygiene report.
alwaysAllow:
  - Bash
  - Read
---

# Repo Hygiene

Review a repository like an operator, not a tourist.

## Objective

Leave the target repo:
- easier to reason about
- lighter on stale worktrees and branches
- explicit about what is still active
- documented with a clear summary report

## Essential Principles

1. **Policy first.** Prefer the repo's own hygiene scripts and Bun aliases before raw git deletion commands.
2. **Safe bucket only by default.** Auto-clean only worktrees and branches already merged into both local `main` and `origin/main`.
3. **Dirty work is a review problem, not a deletion problem.** Flag it clearly instead of guessing.
4. **One report, one source of truth.** Finish with a markdown report that records actions taken, unresolved risks, and next moves.

## When To Use

Use this skill when:
- a repo has accumulated many local worktrees or branches
- the user asks for cleanup, stale branch pruning, or worktree hygiene
- you need to identify branches already merged into both local `main` and `origin/main`
- you need to find unresolved merge conflicts across worktrees
- you need to flag dirty trees before broader cleanup
- you need a markdown report of repo hygiene status and actions

## Read In This Order

1. `workflows/run-repo-hygiene.md` — the execution procedure
2. `references/git-command-playbook.md` — copy-paste command patterns
3. `references/report-template.md` — the final report shape

## Quick Start

1. Confirm the target repo root.
2. Open `workflows/run-repo-hygiene.md` and follow it in order.
3. If the repo ships a local worktree policy, initialize it once before cleanup.
4. Prefer repo-native Bun aliases such as `bun run git:hygiene:json` and `bun run worktree:check` when available.
5. Use the playbook for low-level command snippets.
6. Finish with the report template.

## Multi-Agent Shape

If team or delegation tools are available, split the audit into three small specialist passes:

1. **Refs agent**
   - inspects local branches, upstream tracking, merged state, and `: gone` remotes
2. **Worktree agent**
   - inspects `git worktree list --porcelain`, cleanliness, and branch attachment
3. **Conflict agent**
   - scans every worktree for unmerged paths and unresolved merge states

Then merge those findings into one cleanup plan before mutating anything.

If multi-agent tools are not available, run the same three passes sequentially.

## Cleanup Rules

### Safe to remove by default

- clean worktrees whose branch is merged into both local `main` and `origin/main`
- merged local branches with no attached worktree
- duplicate clean worktrees of the same branch when one canonical keeper remains

### Needs review first

- any dirty worktree
- any branch with unique commits ahead of `main`
- conflicted worktrees not clearly temporary
- branches without upstream if they are not yet merged
- repos whose current root branch is dirty or behind upstream

## Success Criteria

A complete run should leave behind:
- a short executive summary
- a list of actions taken
- a list of flagged dirty trees and conflicts
- a worktree hygiene recommendation set
- a markdown report path

## Optional Install

To promote this workspace skill into a reusable global skill later:

```bash
bun run scripts/install-skill-from-dir.ts \
  --src skills/repo-hygiene \
  --dest ~/.vesper/skills \
  --force
```
