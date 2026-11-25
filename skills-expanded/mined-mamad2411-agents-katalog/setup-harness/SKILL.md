---
name: setup-harness
description: "Wire this repo for the harness delivery loop — agent hooks, merge automation, and worktree cleanup. Run once before the first /implement."
disable-model-invocation: true
---

# Set up harness

`/implement` carries a ticket through review to merge. Three things around it
are properties of the repository rather than of the skill:

- **Agent hooks** — the file-size hints and the handoff guard, wired into Codex
  and Cursor
- **Merge automation** — what merges a pull request once its conditions hold,
  so the agent never merges its own work
- **Worktree cleanup** — what a repository releases when a merged worktree goes
  away

This is a prompt-driven skill, not a deterministic script. Explore, present what
you found, confirm with the user, then write. The configuration is the working
files themselves; this skill writes no documentation describing them.

## Process

### 1. Explore

Read what exists; assume nothing:

- `git remote -v` — a GitHub repository? Which one? Which default branch?
- `.codex/hooks.json` and `.cursor/hooks.json` — hooks this repository already
  runs, harness-owned or not.
- `.mergify.yml` — present? What does it already merge on?
- Who merged the last few pull requests: `gh pr list --state merged --limit 5
  --json number,mergedBy`. A bot login means merge automation is already
  installed and running; only your account means nothing merges on its own.
- `.github/workflows/` — the job names that report as checks. These are the
  candidates for named merge conditions.
- `.agents/hooks/cleanup` — this skill's prior output.
- `git worktree list` and the repository's own scripts — does a linked worktree
  receive resources of its own, such as a database, a port, or a generated
  environment file? A checkout hook under `core.hooksPath` that provisions
  anything is the strongest signal.
- How the repository runs its checks, from `AGENTS.md`, `CLAUDE.md`,
  `package.json` scripts, a `Makefile`, or `scripts/`. `/implement` opens on
  this command, so confirm it is findable rather than recording it anywhere.

### 2. Wire the hooks

Run this skill's `scripts/install_hooks.py`. It points both agents at the hooks
inside this skill and preserves every other hook the repository already ran, so
`npx skills@latest update` is the whole update story: the configuration keeps
naming a path whose contents the update refreshes. It rewrites the same bytes
every run, so ask nothing here and run it whether or not the hooks are already
wired.

### 3. Present findings and ask

Summarise what is present and what is missing. Then take the sections in order —
one section, one answer, then the next. Lead each section with the recommended
answer so the user can accept it in a word, and skip a section outright when
exploration already settled it.

On a repeat run the recommended answer is whatever the repository already
carries: propose keeping it, and write a file only where the user asks for a
change. Running this skill again leaves a hand-tuned configuration as it is.

**Section A — Merge automation.**

> Explainer: `/implement` makes every merge condition hold and waits.
> Something else does the merging. Mergify is the default here because GitHub's
> own required checks and auto-merge need a paid plan on a private repository.

Recommended: Mergify, gated on the checks this repository actually requires.
Take the job names found in `.github/workflows/` and propose the ones that must
pass — usually the test or integration job, not a job that only runs for some
changes. Write [`mergify.yml`](./mergify.yml), substituting the default branch
and one `check-success` line per required check.

Offer these alternatives:

- **Count checks instead of naming them** — replace the `check-success` lines
  with `#check-failure = 0` and `#check-pending = 0`. It survives a workflow
  being renamed, at the cost of a race: a pull request whose checks have not
  been created yet satisfies both counts. Propose it only when the required set
  genuinely varies.
- **No automation** — the reviewer merges by hand while `/implement` waits.

When `.mergify.yml` already exists, change only the rule this skill owns and
leave the rest of the file as it stands.

Mergify merges nothing until its GitHub App is installed on the repository. If
exploration found no bot merges, say so and point the user at
https://github.com/apps/mergify.

**Section B — Worktree cleanup.** Skip this section entirely when exploration
found no per-worktree resources — `/implement` already removes the merged
worktree and its branch, and a repository that owns nothing else needs no hook.

Otherwise ask one question:

> Which command releases what a worktree owned, once the worktree is gone?

Write it as an executable `.agents/hooks/cleanup`, using [`cleanup`](./cleanup)
as the starting point with its `RELEASE_COMMAND` placeholder replaced by the
answer. `/implement` runs it after removing a merged worktree and reports its
output, so have the command name what it released rather than working silently.

### 4. Confirm and write

Show the user each file you are about to write and let them edit it first. Then
write them, and make `.agents/hooks/cleanup` executable.

### 5. Done

Tell the user to commit the generated files so the tooling stays a property of
the repository, and that Codex needs `/hooks` to trust the project hook once
while Cursor reloads `.cursor/hooks.json` on save. Updating the tooling itself is
`npx skills@latest update`; this skill is worth running again to change how the
repository merges or what it releases, and safe to run again for any reason.
