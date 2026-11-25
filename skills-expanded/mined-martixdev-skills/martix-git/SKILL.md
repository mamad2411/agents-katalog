---
name: martix-git
description: 'Safe Git and GitHub lifecycle guidance. Use when a request involves Conventional Commits, commit-message review, Conventional Branch naming, branch or worktree decisions, staged commits, pull-request drafting or creation, issue references, SemVer, semantic-release, Git hooks, commitlint, lint-staged, pre-commit or pre-push gates, worktree audits, post-merge cleanup, or local versus remote branch cleanup.'
license: Complete terms in LICENSE.txt
---

# MartiX Git router

Use this skill for Git workflow and GitHub lifecycle decisions where policy,
release history, hooks, pull requests, or worktree safety matters. Start with
one primary workflow, inspect the smallest relevant repository state, and route
to one rule or reference file before widening context.

## Boundary

In scope: Conventional Commits 1.0.0, Conventional Branch v1.1.0, Git branch
and worktree practice, staged commit planning, GitHub pull requests and issue
links, SemVer 2.0.0, optional semantic-release integration, native hooks and
CI quality gates, and report-first worktree cleanup.

Out of scope: generic application version parsing, unrelated file deletion,
general CI/CD or deployment design, interactive rebase, Sandcastle lifecycle
management, or replacing Git, `gh`, GitHub protection, repository CI, Husky,
lint-staged, or commitlint.

## Route by intent

| Request | Start here | Add only when needed |
| --- | --- | --- |
| Bare `/martix-git`, status, or unclear Git request | [smart-command-map.md](./references/smart-command-map.md) | The closest workflow rule |
| Commit message, staged diff, breaking change, or commit policy | [conventional-commits.md](./rules/conventional-commits.md) | [git-workflows-and-hooks.md](./rules/git-workflows-and-hooks.md) |
| Branch name, topic branch, trunk, or ref validation | [conventional-branches.md](./rules/conventional-branches.md) | [smart-command-map.md](./references/smart-command-map.md) |
| Composed `/martix-git pr` branch-to-PR or multi-phase repository workflow | [smart-command-map.md](./references/smart-command-map.md) | [git-workflows-and-hooks.md](./rules/git-workflows-and-hooks.md), [pull-requests-and-issues.md](./rules/pull-requests-and-issues.md) |
| Pull request, title, body, merge policy, or issue link | [pull-requests-and-issues.md](./rules/pull-requests-and-issues.md) | [git-workflows-and-hooks.md](./rules/git-workflows-and-hooks.md) |
| SemVer, tags, release impact, or semantic-release | [semver-and-semantic-release.md](./rules/semver-and-semantic-release.md) | [source-map.md](./references/source-map.md) |
| Hook setup, commitlint, lint-staged, CI, or protection | [git-workflows-and-hooks.md](./rules/git-workflows-and-hooks.md) | [smart-command-map.md](./references/smart-command-map.md) |
| Worktree audit, stale branch, or cleanup | [worktree-lifecycle.md](./rules/worktree-lifecycle.md) | [smart-command-map.md](./references/smart-command-map.md) |

## Operating contract

1. Label the evidence as a source requirement, repository policy,
   recommendation, inference, or unresolved gap.
2. Inspect status, branch, staged diff, upstream, relevant policy, and remote
   evidence only when the requested workflow needs them.
3. Build a structured plan with `perform`, `skip`, `ask`, or `block` for every
   relevant phase.
4. Show proposed commands, exact targets, assumptions, and expected effects.
5. Obtain confirmation before each state-changing action, or before a grouped
   set of displayed actions.
6. Re-read state after every mutation and recompute dependent phases.
7. Report completed, skipped, blocked, failed, and unresolved results separately.

The no-argument `/martix-git` entrypoint is read-only when intent is absent. A
dirty worktree alone never authorizes staging, committing, branching, pushing,
PR creation, release publication, or cleanup.

## Safety floor

Use argument-based Git and GitHub CLI invocation, temporary files for
multi-line messages, and bounded output. Preserve uncertain, dirty, locked,
current, protected, detached, active, externally owned, open-PR, and unknown
states. Do not use force push, `reset --hard`, `clean -fd`, force deletion,
empty commits, implicit staging, hook bypass, or duplicate PR creation as a
hidden fallback.

For cleanup, audit first and revalidate immediately before each selected
mutation. Local worktree and branch cleanup is separate from remote branch and
PR cleanup. The existing [git-cleanup.ps1](../../scripts/git-cleanup.ps1) is the
initial repository reference engine; do not invent competing cleanup semantics.

## Near misses

Do not route a request only because it contains `commit`, `branch`, or
`release`. Generic application version parsing, deleting an unrelated file, or
ordinary Git usage without policy, GitHub, release, hook, or worktree concerns
belongs to the normal coding workflow.

## Completion

A useful answer identifies the route, current evidence, policy boundary,
proposed result or command, confirmation point, validation performed, and any
remaining uncertainty. Never claim that a command ran when it was only drafted.
Use [AGENTS.md](./AGENTS.md) for maintainer routes and package boundaries.
