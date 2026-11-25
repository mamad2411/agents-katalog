---
name: pr-splitter
description: Decompose large, complex pull requests into atomic, logically isolated, reviewable PR branches.
category: development
aliases:
- split-pr
- atomic-pr
- decompose-pr
- pr-slice
triggers:
- split this PR
- break down large pull request
- decompose PR into smaller chunks
- make this PR reviewable
- slice this diff
keywords:
- pr
- pull-request
- split
- atomic
- diff
- review
- branch
- git
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities:
- pr-splitting
- diff-decomposition
- atomic-branching
inputs:
- git_diff
- branch
- target_branch
outputs:
- split_plan
- branch_sequence
- dependency_graph
permissions:
  filesystem: none
  network: none
  shell: none
  secrets: none
author: Mr-Nobody-Anonymous
tags:
- atomic
- development
- pull-request
- split
- splitter
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# PR Splitter

## Purpose
Decomposes large, monolithic diffs and pull requests into small, atomic, reviewable PR branches. This accelerates code review velocity, reduces merge conflicts, and isolates regression risks.

## When to Use
- Pull request exceeds 400 lines of modified code.
- A feature branch mixes architectural refactoring, database migrations, and UI changes.
- Reviewers are blocked by the sheer cognitive load of a massive diff.
- Stacked PR or progressive rollout workflows are required.

## When NOT to Use
- Small, tightly coupled changes that cannot be separated without breaking the build.
- Single-commit bugfixes under 50 lines.

## Capabilities
- **Diff Analysis**: Parse git diffs and group modifications by component, schema, and dependency layers.
- **Dependency Graphing**: Determine safe branch merge orders to prevent intermediate breakage.
- **Stacked Branch Creation**: Scaffold stacked git branches with independent commit baselines.
- **Reviewer Guidance**: Generate clear review summaries for each incremental slice.

## Inputs
- `git_diff` (required) — Full diff or branch reference to inspect.
- `target_branch` (optional) — Base branch (default: `main`).
- `max_pr_size` (optional) — Soft ceiling for lines of code per split PR (default: 250).

## Workflow
1. Inspect the complete diff and identify discrete conceptual layers (e.g., contracts, models, backend logic, tests, frontend UI).
2. Establish a linear or tree-based dependency order between layers.
3. Slice changes into isolated commit ranges that maintain a passing test suite at each step.
4. Prepare branch names, commit messages, and PR descriptions indicating dependencies (`Depends on PR #X`).
5. Verify that each sliced branch builds cleanly in isolation.

## Tools
- `git` for branch creation, cherry-picking, and diff analysis.

## Examples
- "This branch has 1,200 lines across 15 files; split this PR into reviewable chunks."
- "Decompose my refactoring and new feature implementation into stacked PRs."
- "Slice this diff so our backend migration can be reviewed before the frontend work."

## Safety
- Never leave intermediate branches with broken unit tests or broken compilation.
- Ensure uncommitted local changes are stashed or committed before checking out split branches.

## Source
Custom skill maintained in this library following modular Git workflow standards.

## Notes
Pairs synergistically with `development.git-workflow` and `development.requesting-code-review`.
