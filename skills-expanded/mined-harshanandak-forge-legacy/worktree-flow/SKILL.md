---
name: worktree-flow
description: >
  Use before starting any Forge code change, and whenever a second agent is
  about to work in the same repo — creating, entering, or cleaning an isolated
  worktree. Do not use raw `git worktree add`; it creates a branch and nothing
  else.
---

# worktree-flow

Two agents in one checkout collide on HEAD mid-task. The isolation is not
optional and the primary checkout is not yours. [Forge #6 ×4]

## Create

```bash
forge worktree create <slug>
```

Run it from the **primary repo root** — create and clean are cwd-scoped.
`forge worktree create` does three things raw `git worktree add` does not: it
links the kernel issue, sets up the issue store, and wires dependencies.
[Forge #6 ×4]

Then work entirely inside `.worktrees/<slug>/`.

## Two things that bite on Windows

- **`node_modules` is a root-only junction.** A fresh worktree is missing
  `packages/skills/node_modules`; junction it or the skills tests fail on a
  missing `chalk`/`inquirer`.
- **Long paths.** After `git worktree remove --force`, a leftover directory may
  need a `\\?\`-prefixed delete.

## Clean

```bash
forge clean
```

Fast-forward local `main`/`master` first, or squash-merge detection misses your
branch and the worktree is left behind. `forge clean` has no default-branch
guard — run it from the primary root and know which branch you are on.

## Working alongside other agents

- One agent, one worktree, one PR. Two agents leading the same PR is a
  correction Harsha has made repeatedly. [Forge #6 ×4]
- Parallel agents state file ownership up front, before either starts editing.
- **Never call another agent dead from one sample.** A clean tree and no recent
  writes also describes an agent between a commit and its next red test. Sample
  twice, minutes apart, and compare. Any respawn must refuse to edit a contended
  worktree.
- If you are asked to work in the primary checkout while another stream is
  live, say no and create a worktree.

## Done when

Your changes live on a branch inside `.worktrees/<slug>/`, the primary checkout
is untouched, and the worktree either has an open PR or has been cleaned.
